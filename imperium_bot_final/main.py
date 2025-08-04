"""
Arquivo principal do Imperium™ Bot
Inicializa o bot, carrega handlers e configura serviços
"""

import asyncio
import sys
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.settings import BOT_TOKEN, validate_config
from database.models import db_manager
from utils.logger import logger
from handlers import start_handler, payment_handler
from admin_panel.scheduler import scheduler

async def main():
    """Função principal do bot"""
    try:
        # Validar configurações
        logger.info("Iniciando Imperium™ Bot...")
        validate_config()
        logger.info("✅ Configurações validadas")
        
        # Inicializar banco de dados
        await db_manager.init_database()
        logger.info("✅ Banco de dados inicializado")
        
        # Configurar bot
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Configurar dispatcher
        dp = Dispatcher(storage=MemoryStorage())
        
        # Registrar handlers
        dp.include_router(start_handler.router)
        dp.include_router(payment_handler.router)
        
        # Iniciar scheduler
        scheduler.start()
        logger.info("✅ Scheduler iniciado")
        
        # Log de startup
        await logger.log_system_event("STARTUP", "Bot iniciado com sucesso")
        
        # Iniciar polling
        logger.info("🚀 Bot iniciado! Pressione Ctrl+C para parar.")
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        await logger.log_system_event("ERROR", f"Erro crítico: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if 'scheduler' in locals():
            scheduler.shutdown()
        await logger.log_system_event("SHUTDOWN", "Bot finalizado")
        logger.info("👋 Bot finalizado")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot interrompido")
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)