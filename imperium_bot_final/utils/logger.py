"""
Sistema de logs local e remoto para o Imperium™ Bot
Implementa logging local em arquivo e envio para canal do Telegram
"""

import logging
import asyncio
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler
from aiogram import Bot
from config.settings import CANAL_LOGS_ID, BOT_TOKEN, LOG_FORMAT, LOG_FILE

class TelegramLogHandler(logging.Handler):
    """Handler personalizado para enviar logs para o Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = None
        self._log_queue = []
        self._processing = False
    
    async def _init_bot(self):
        """Inicializa o bot se necessário"""
        if not self.bot:
            self.bot = Bot(token=self.bot_token)
    
    def emit(self, record):
        """Envia log para o Telegram de forma assíncrona"""
        if record.levelno >= logging.WARNING:  # Apenas WARNING, ERROR e CRITICAL
            try:
                # Adicionar à fila de logs
                self._log_queue.append(record)
                
                # Processar fila se não estiver processando
                if not self._processing:
                    asyncio.create_task(self._process_log_queue())
            except Exception:
                pass  # Não gerar erro se falhar o log remoto
    
    async def _process_log_queue(self):
        """Processa a fila de logs para envio"""
        if self._processing:
            return
        
        self._processing = True
        
        try:
            await self._init_bot()
            
            while self._log_queue:
                record = self._log_queue.pop(0)
                await self._send_log_message(record)
                await asyncio.sleep(1)  # Evitar spam
        except Exception:
            pass  # Falha silenciosa para não quebrar o bot
        finally:
            self._processing = False
    
    async def _send_log_message(self, record):
        """Envia mensagem de log para o Telegram"""
        try:
            # Formatr mensagem de log
            message = self._format_telegram_message(record)
            
            if len(message) > 4096:  # Limite do Telegram
                message = message[:4090] + "..."
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML"
            )
        except Exception:
            pass  # Falha silenciosa
    
    def _format_telegram_message(self, record) -> str:
        """Formata mensagem de log para o Telegram"""
        # Emoji por nível de log
        emoji_map = {
            logging.DEBUG: "🔍",
            logging.INFO: "ℹ️",
            logging.WARNING: "⚠️",
            logging.ERROR: "❌", 
            logging.CRITICAL: "🚨"
        }
        
        emoji = emoji_map.get(record.levelno, "📝")
        timestamp = datetime.fromtimestamp(record.created).strftime("%d/%m/%Y %H:%M:%S")
        
        message = f"{emoji} <b>{record.levelname}</b>\n"
        message += f"🕐 <i>{timestamp}</i>\n"
        message += f"📁 <code>{record.name}</code>\n"
        message += f"💬 {record.getMessage()}\n"
        
        if record.exc_info:
            message += f"🔥 <code>{record.exc_text}</code>"
        
        return message

class ImperiumLogger:
    """Classe principal para gerenciamento de logs"""
    
    def __init__(self):
        self.logger = None
        self.telegram_handler = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura o sistema de logs"""
        # Criar diretório de logs se não existir
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        # Configurar logger principal
        self.logger = logging.getLogger('imperium_bot')
        self.logger.setLevel(logging.DEBUG)
        
        # Limpar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para arquivo local com rotação
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para Telegram (se configurado)
        if BOT_TOKEN and CANAL_LOGS_ID:
            try:
                self.telegram_handler = TelegramLogHandler(BOT_TOKEN, CANAL_LOGS_ID)
                self.telegram_handler.setLevel(logging.WARNING)
                self.logger.addHandler(self.telegram_handler)
            except Exception as e:
                self.logger.warning(f"Não foi possível configurar logs remotos: {e}")
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log informativo"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log de erro"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log crítico"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """Log de exceção com traceback"""
        self.logger.exception(message)
    
    async def log_user_action(self, user_id: int, action: str, details: str = ""):
        """Log específico para ações de usuários"""
        message = f"Usuário {user_id} - {action}"
        if details:
            message += f" - {details}"
        self.info(message)
    
    async def log_payment_event(self, user_id: int, payment_id: str, 
                               event: str, amount: float = None):
        """Log específico para eventos de pagamento"""
        message = f"Pagamento {payment_id} - Usuário {user_id} - {event}"
        if amount:
            message += f" - R$ {amount:.2f}"
        self.info(message)
        
        # Eventos importantes vão para o Telegram
        if event in ["APROVADO", "ERRO", "EXPIRADO"]:
            self.warning(message)
    
    async def log_affiliate_event(self, affiliate_id: int, referred_user_id: int, 
                                 event: str, commission: float = None):
        """Log específico para eventos de afiliados"""
        message = f"Afiliado {affiliate_id} - Indicado {referred_user_id} - {event}"
        if commission:
            message += f" - Comissão: R$ {commission:.2f}"
        self.info(message)
        
        if event in ["NOVA_VENDA", "SAQUE_SOLICITADO"]:
            self.warning(message)
    
    async def log_admin_action(self, admin_id: int, action: str, target: str = ""):
        """Log específico para ações administrativas"""
        message = f"Admin {admin_id} - {action}"
        if target:
            message += f" - {target}"
        self.warning(message)  # Ações de admin sempre vão para Telegram
    
    async def log_system_event(self, event: str, details: str = ""):
        """Log de eventos do sistema"""
        message = f"Sistema - {event}"
        if details:
            message += f" - {details}"
        self.info(message)
        
        # Eventos críticos do sistema
        if event in ["STARTUP", "SHUTDOWN", "ERROR", "DATABASE_ERROR"]:
            self.warning(message)
    
    async def send_daily_report(self, stats: dict):
        """Envia relatório diário para o canal de logs"""
        try:
            report = "📊 <b>RELATÓRIO DIÁRIO - IMPERIUM™</b>\n\n"
            report += f"👥 Usuários totais: <b>{stats.get('total_users', 0)}</b>\n"
            report += f"🆕 Novos usuários hoje: <b>{stats.get('users_today', 0)}</b>\n"
            report += f"💎 Assinaturas ativas: <b>{stats.get('active_subscriptions', 0)}</b>\n"
            report += f"💰 Faturamento total: <b>R$ {stats.get('total_revenue', 0):.2f}</b>\n"
            report += f"📈 Faturamento hoje: <b>R$ {stats.get('revenue_today', 0):.2f}</b>\n"
            report += f"💸 Saques pendentes: <b>{stats.get('pending_withdrawals', 0)}</b>\n"
            report += f"\n🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
            
            if self.telegram_handler and self.telegram_handler.bot:
                await self.telegram_handler.bot.send_message(
                    chat_id=CANAL_LOGS_ID,
                    text=report,
                    parse_mode="HTML"
                )
            
            self.info("Relatório diário enviado")
        except Exception as e:
            self.error(f"Erro ao enviar relatório diário: {e}")
    
    async def send_alert(self, title: str, message: str, level: str = "warning"):
        """Envia alerta específico para o canal"""
        try:
            emoji_map = {
                "info": "ℹ️",
                "warning": "⚠️", 
                "error": "❌",
                "critical": "🚨"
            }
            
            emoji = emoji_map.get(level, "📢")
            alert_text = f"{emoji} <b>{title}</b>\n\n{message}\n\n🕐 {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
            
            if self.telegram_handler and self.telegram_handler.bot:
                await self.telegram_handler.bot.send_message(
                    chat_id=CANAL_LOGS_ID,
                    text=alert_text,
                    parse_mode="HTML"
                )
            
            # Também logar localmente
            getattr(self, level, self.info)(f"{title}: {message}")
        except Exception as e:
            self.error(f"Erro ao enviar alerta: {e}")
    
    def get_log_stats(self) -> dict:
        """Obtém estatísticas dos logs"""
        try:
            if not os.path.exists(LOG_FILE):
                return {"size": 0, "lines": 0}
            
            size = os.path.getsize(LOG_FILE)
            
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = sum(1 for line in f)
            
            return {
                "size": size,
                "lines": lines,
                "size_mb": size / (1024 * 1024)
            }
        except Exception as e:
            self.error(f"Erro ao obter estatísticas dos logs: {e}")
            return {"size": 0, "lines": 0}
    
    def cleanup_old_logs(self, days: int = 30):
        """Remove logs antigos"""
        try:
            log_dir = os.path.dirname(LOG_FILE)
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            for filename in os.listdir(log_dir):
                filepath = os.path.join(log_dir, filename)
                if os.path.isfile(filepath) and filename.endswith('.log'):
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        self.info(f"Log antigo removido: {filename}")
        except Exception as e:
            self.error(f"Erro ao limpar logs antigos: {e}")

# Instância global do logger
logger = ImperiumLogger()