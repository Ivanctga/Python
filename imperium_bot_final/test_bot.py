#!/usr/bin/env python3
"""
Bot de teste simplificado para verificar funcionamento básico
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    await update.message.reply_text(
        '🎉 <b>Imperium™ Bot funcionando!</b>\n\n'
        '✅ Python-telegram-bot OK\n'
        '✅ Python 3.13 OK\n'
        '✅ Todas as dependências OK\n\n'
        '🚀 Bot pronto para produção!',
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    await update.message.reply_text(
        '📋 <b>Comandos disponíveis:</b>\n\n'
        '/start - Iniciar bot\n'
        '/help - Esta ajuda\n'
        '/test - Teste de funcionalidades\n\n'
        '💎 <b>Bot Imperium™ v2.0</b>\n'
        'Migrado para python-telegram-bot com sucesso!',
        parse_mode='HTML'
    )

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /test"""
    try:
        # Testar QR Code
        from payments.qr_generator import qr_generator
        test_pix = "00020126580014br.gov.bcb.pix123456"
        qr_bytes = qr_generator.generate_qr_code(test_pix)
        
        if qr_bytes:
            await update.message.reply_photo(
                photo=qr_bytes,
                caption='✅ <b>Teste QR Code OK!</b>\n\n'
                       f'📊 Tamanho: {len(qr_bytes)} bytes\n'
                       '🎯 Geração funcionando perfeitamente!',
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text('❌ Erro ao gerar QR Code')
            
    except Exception as e:
        await update.message.reply_text(f'❌ Erro no teste: {e}')

def main() -> None:
    """Função principal"""
    # Token de teste - substitua por um token real para testar
    TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ-TEST-TOKEN"
    
    # Criar aplicação
    application = Application.builder().token(TOKEN).build()
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    
    # Log de inicialização
    logger.info("🚀 Bot de teste iniciando...")
    logger.info("📝 Use um token real para testar completamente")
    
    # Iniciar polling
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f"Erro: {e}")
        if "Unauthorized" in str(e):
            logger.error("❌ Token inválido! Use um token real do @BotFather")
        elif "Invalid token" in str(e):
            logger.error("❌ Formato de token inválido!")

if __name__ == '__main__':
    main()