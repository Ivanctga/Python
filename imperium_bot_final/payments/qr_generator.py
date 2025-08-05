"""
Gerador de QR Code sem dependência do Pillow
Versão simplificada para compatibilidade máxima
"""

import qrcode
import io
import os
import platform
from typing import Optional
from utils.logger import logger

class QRCodeGenerator:
    def __init__(self):
        """Inicializa o gerador de QR Code"""
        self.system = platform.system().lower()
        logger.info(f"QR Code Generator inicializado para sistema: {self.system}")
    
    def generate_qr_code(self, data: str) -> Optional[bytes]:
        """
        Gera QR Code como imagem bytes (versão simplificada)
        
        Args:
            data: Dados para o QR Code (código Pix)
        
        Returns:
            Bytes da imagem do QR Code ou None se erro
        """
        try:
            # Configurações do QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Gerar imagem do QR Code
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para bytes
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            logger.info("QR Code gerado com sucesso")
            return img_bytes
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code: {e}")
            return self._generate_fallback_qr(data)
    
    def generate_qr_with_info(self, pix_data: str, amount: float, 
                             description: str = "Imperium™") -> Optional[bytes]:
        """
        Gera QR Code básico (versão simplificada sem informações adicionais)
        
        Args:
            pix_data: Código Pix
            amount: Valor do pagamento (não usado nesta versão simplificada)
            description: Descrição do pagamento (não usado nesta versão simplificada)
        
        Returns:
            Bytes da imagem do QR Code
        """
        try:
            # Gerar QR Code básico
            return self.generate_qr_code(pix_data)
            
        except Exception as e:
            logger.error(f"Erro ao gerar QR Code com informações: {e}")
            return self.generate_qr_code(pix_data)
    
    def _generate_fallback_qr(self, data: str) -> Optional[bytes]:
        """
        Gera QR Code usando método de fallback mais simples
        
        Args:
            data: Dados para o QR Code
        
        Returns:
            Bytes da imagem ou None se falhar
        """
        try:
            logger.info("Gerando QR Code usando método de fallback")
            
            # QR Code mais simples sem customizações
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=2,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Gerar imagem básica
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            
            logger.info("QR Code de fallback gerado com sucesso")
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Erro no fallback do QR Code: {e}")
            return None
    
    def validate_qr_data(self, data: str) -> bool:
        """
        Valida se os dados são adequados para QR Code
        
        Args:
            data: Dados a serem validados
        
        Returns:
            True se válidos, False caso contrário
        """
        try:
            # Verificar tamanho dos dados
            if len(data) > 2000:  # Limite prático para QR Code
                logger.warning("Dados muito longos para QR Code")
                return False
            
            # Verificar se não está vazio
            if not data.strip():
                logger.warning("Dados vazios para QR Code")
                return False
            
            # Tentar gerar QR Code para teste
            test_qr = qrcode.QRCode(version=1)
            test_qr.add_data(data)
            test_qr.make(fit=True)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao validar dados do QR Code: {e}")
            return False

# Instância global do gerador de QR Code
qr_generator = QRCodeGenerator()