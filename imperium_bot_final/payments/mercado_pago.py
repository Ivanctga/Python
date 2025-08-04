"""
Integração com Mercado Pago para processamento de pagamentos Pix
Implementa criação de pagamentos e verificação de status
"""

import mercadopago
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from config.settings import MP_ACCESS_TOKEN, MP_PUBLIC_KEY
from utils.logger import logger

class MercadoPagoPayment:
    def __init__(self):
        """Inicializa a integração com Mercado Pago"""
        try:
            self.sdk = mercadopago.SDK(MP_ACCESS_TOKEN)
            logger.info("SDK do Mercado Pago inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar SDK do Mercado Pago: {e}")
            raise
    
    def create_pix_payment(self, user_id: int, user_phone: str, amount: float, 
                          plan_name: str, description: str = None) -> Optional[Dict]:
        """
        Cria um pagamento Pix no Mercado Pago
        
        Args:
            user_id: ID do usuário do Telegram
            user_phone: Telefone do usuário para contato
            amount: Valor do pagamento
            plan_name: Nome do plano selecionado
            description: Descrição do produto (opcional)
        
        Returns:
            Dict com dados do pagamento criado ou None se erro
        """
        try:
            # Gerar ID único para o pagamento
            external_reference = f"IMPERIUM_{user_id}_{int(datetime.now().timestamp())}"
            
            # Descrição padrão se não fornecida
            if not description:
                description = f"Imperium™ - Plano {plan_name}"
            
            # Dados do pagamento
            payment_data = {
                "transaction_amount": float(amount),
                "description": description,
                "payment_method_id": "pix",
                "external_reference": external_reference,
                "payer": {
                    "email": f"user{user_id}@imperium.com",  # Email fictício
                    "phone": {
                        "area_code": user_phone[:2] if len(user_phone) >= 10 else "11",
                        "number": user_phone[2:] if len(user_phone) >= 10 else user_phone
                    },
                    "identification": {
                        "type": "CPF",
                        "number": "00000000000"  # CPF fictício para testes
                    }
                },
                "notification_url": f"https://webhook.site/unique-id",  # Substitua por sua URL
                "date_of_expiration": (datetime.now() + timedelta(hours=24)).isoformat(),
                "metadata": {
                    "user_id": str(user_id),
                    "plan_name": plan_name,
                    "phone": user_phone
                }
            }
            
            # Criar pagamento
            logger.info(f"Criando pagamento Pix para usuário {user_id}, valor: R$ {amount}")
            
            payment_response = self.sdk.payment().create(payment_data)
            payment = payment_response["response"]
            
            if payment_response["status"] == 201:
                logger.info(f"Pagamento criado com sucesso. ID: {payment['id']}")
                
                # Extrair dados do QR Code Pix
                qr_code_data = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code", "")
                qr_code_base64 = payment.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64", "")
                
                return {
                    "id": str(payment["id"]),
                    "status": payment["status"],
                    "amount": payment["transaction_amount"],
                    "qr_code_data": qr_code_data,
                    "qr_code_base64": qr_code_base64,
                    "external_reference": external_reference,
                    "created_date": payment["date_created"],
                    "expiration_date": payment.get("date_of_expiration"),
                    "payment_url": payment.get("point_of_interaction", {}).get("transaction_data", {}).get("ticket_url", "")
                }
            else:
                logger.error(f"Erro ao criar pagamento: {payment_response}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao criar pagamento Pix: {e}")
            return None
    
    def check_payment_status(self, payment_id: str) -> Optional[Dict]:
        """
        Verifica o status de um pagamento no Mercado Pago
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            Dict com status do pagamento ou None se erro
        """
        try:
            logger.info(f"Verificando status do pagamento: {payment_id}")
            
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                payment = payment_response["response"]
                
                # Status possíveis: pending, approved, authorized, in_process, 
                # in_mediation, rejected, cancelled, refunded, charged_back
                status_info = {
                    "id": str(payment["id"]),
                    "status": payment["status"],
                    "status_detail": payment.get("status_detail", ""),
                    "amount": payment["transaction_amount"],
                    "currency_id": payment["currency_id"],
                    "date_created": payment["date_created"],
                    "date_approved": payment.get("date_approved"),
                    "date_last_updated": payment["date_last_updated"],
                    "external_reference": payment.get("external_reference", ""),
                    "description": payment.get("description", ""),
                    "metadata": payment.get("metadata", {})
                }
                
                logger.info(f"Status do pagamento {payment_id}: {payment['status']}")
                return status_info
            else:
                logger.error(f"Erro ao consultar pagamento: {payment_response}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao verificar status do pagamento {payment_id}: {e}")
            return None
    
    def is_payment_approved(self, payment_id: str) -> bool:
        """
        Verifica se um pagamento foi aprovado
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            True se aprovado, False caso contrário
        """
        try:
            status_info = self.check_payment_status(payment_id)
            if status_info:
                return status_info["status"] == "approved"
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar aprovação do pagamento {payment_id}: {e}")
            return False
    
    def is_payment_pending(self, payment_id: str) -> bool:
        """
        Verifica se um pagamento está pendente
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            True se pendente, False caso contrário
        """
        try:
            status_info = self.check_payment_status(payment_id)
            if status_info:
                return status_info["status"] in ["pending", "in_process"]
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar se pagamento está pendente {payment_id}: {e}")
            return False
    
    def is_payment_expired(self, payment_id: str) -> bool:
        """
        Verifica se um pagamento expirou
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            True se expirado, False caso contrário
        """
        try:
            status_info = self.check_payment_status(payment_id)
            if status_info:
                # Verificar se foi rejeitado ou cancelado
                if status_info["status"] in ["rejected", "cancelled"]:
                    return True
                
                # Verificar se expirou por tempo
                date_created = datetime.fromisoformat(status_info["date_created"].replace("Z", "+00:00"))
                expiration_time = date_created + timedelta(hours=24)
                
                return datetime.now() > expiration_time.replace(tzinfo=None)
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar expiração do pagamento {payment_id}: {e}")
            return False
    
    def get_payment_time_remaining(self, payment_id: str) -> str:
        """
        Calcula o tempo restante para expiração do pagamento
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            String formatada com tempo restante
        """
        try:
            status_info = self.check_payment_status(payment_id)
            if status_info:
                date_created = datetime.fromisoformat(status_info["date_created"].replace("Z", "+00:00"))
                expiration_time = date_created + timedelta(hours=24)
                now = datetime.now()
                
                if now < expiration_time.replace(tzinfo=None):
                    remaining = expiration_time.replace(tzinfo=None) - now
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    return f"{hours}h {minutes}min"
                else:
                    return "Expirado"
            return "Não disponível"
        except Exception as e:
            logger.error(f"Erro ao calcular tempo restante do pagamento {payment_id}: {e}")
            return "Erro ao calcular"
    
    def cancel_payment(self, payment_id: str) -> bool:
        """
        Cancela um pagamento no Mercado Pago
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            True se cancelado com sucesso, False caso contrário
        """
        try:
            logger.info(f"Cancelando pagamento: {payment_id}")
            
            cancel_data = {"status": "cancelled"}
            response = self.sdk.payment().update(payment_id, cancel_data)
            
            if response["status"] == 200:
                logger.info(f"Pagamento {payment_id} cancelado com sucesso")
                return True
            else:
                logger.error(f"Erro ao cancelar pagamento: {response}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao cancelar pagamento {payment_id}: {e}")
            return False
    
    def refund_payment(self, payment_id: str, amount: float = None) -> bool:
        """
        Realiza reembolso de um pagamento
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
            amount: Valor a ser reembolsado (None para reembolso total)
        
        Returns:
            True se reembolsado com sucesso, False caso contrário
        """
        try:
            logger.info(f"Processando reembolso do pagamento: {payment_id}")
            
            refund_data = {}
            if amount:
                refund_data["amount"] = amount
            
            response = self.sdk.refund().create(payment_id, refund_data)
            
            if response["status"] == 201:
                logger.info(f"Reembolso do pagamento {payment_id} processado com sucesso")
                return True
            else:
                logger.error(f"Erro ao processar reembolso: {response}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao processar reembolso do pagamento {payment_id}: {e}")
            return False
    
    def get_payment_info(self, payment_id: str) -> Optional[Dict]:
        """
        Obtém informações completas de um pagamento
        
        Args:
            payment_id: ID do pagamento no Mercado Pago
        
        Returns:
            Dict com informações completas do pagamento
        """
        try:
            status_info = self.check_payment_status(payment_id)
            if status_info:
                # Adicionar informações calculadas
                status_info["is_approved"] = self.is_payment_approved(payment_id)
                status_info["is_pending"] = self.is_payment_pending(payment_id)
                status_info["is_expired"] = self.is_payment_expired(payment_id)
                status_info["time_remaining"] = self.get_payment_time_remaining(payment_id)
                
                return status_info
            return None
        except Exception as e:
            logger.error(f"Erro ao obter informações do pagamento {payment_id}: {e}")
            return None

# Instância global do processador de pagamentos
mp_payment = MercadoPagoPayment()