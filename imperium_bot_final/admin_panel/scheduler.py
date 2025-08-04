"""
Agendador de tarefas automáticas para o Imperium™ Bot
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio

from database.models import db_manager
from utils.logger import logger
from config.settings import DAILY_REPORT_TIME, DATABASE_BACKUP_TIME

# Instância global do scheduler
scheduler = AsyncIOScheduler()

async def daily_report():
    """Envia relatório diário"""
    try:
        stats = await db_manager.get_statistics()
        await logger.send_daily_report(stats)
        logger.info("Relatório diário enviado")
    except Exception as e:
        logger.error(f"Erro ao enviar relatório diário: {e}")

async def database_backup():
    """Realiza backup do banco de dados"""
    try:
        import shutil
        from datetime import datetime
        
        backup_name = f"logs/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2("imperium_bot.db", backup_name)
        logger.info(f"Backup realizado: {backup_name}")
    except Exception as e:
        logger.error(f"Erro no backup: {e}")

# Configurar tarefas
def configure_jobs():
    """Configura todas as tarefas agendadas"""
    
    # Relatório diário às 9h
    hour, minute = map(int, DAILY_REPORT_TIME.split(':'))
    scheduler.add_job(
        daily_report,
        CronTrigger(hour=hour, minute=minute),
        id="daily_report",
        replace_existing=True
    )
    
    # Backup às 3h da manhã
    hour, minute = map(int, DATABASE_BACKUP_TIME.split(':'))
    scheduler.add_job(
        database_backup,
        CronTrigger(hour=hour, minute=minute),
        id="database_backup",
        replace_existing=True
    )
    
    logger.info("Tarefas agendadas configuradas")

# Configurar jobs na inicialização
configure_jobs()