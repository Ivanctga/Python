"""
Handler para comando /start e fluxo inicial do Imperium™ Bot
Gerencia entrada de usuários, referências e menu principal
"""

from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from typing import Optional
import os

from database.models import db_manager
from states.user_states import UserStates
from keyboards.inline_keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from config.settings import (
    WELCOME_MESSAGE, ADMIN_IDS, VIP_GROUP_LINK, 
    SUPPORT_CONTACT
)
from utils.helpers import extract_referrer_from_start, get_user_display_name, format_date_br
from utils.logger import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processa comando /start com ou sem parâmetros de referência
    
    Args:
        update: Update do telegram
        context: Context do telegram
    """
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        
        # Extrair referenciador se houver
        referrer_id = None
        if context.args:
            start_param = context.args[0] if context.args else None
            if start_param:
                referrer_id = extract_referrer_from_start(start_param)
                if referrer_id == user_id:
                    referrer_id = None  # Usuário não pode se referenciar
        
        # Verificar se usuário já existe
        existing_user = await db_manager.get_user(user_id)
        
        if not existing_user:
            # Adicionar novo usuário
            success = await db_manager.add_user(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                referrer_id=referrer_id
            )
            
            if success:
                await logger.log_user_action(
                    user_id, 
                    "NOVO_USUARIO", 
                    f"Referenciado por: {referrer_id}" if referrer_id else "Entrada direta"
                )
                
                # Notificar sobre novo usuário se foi referenciado
                if referrer_id:
                    await logger.log_affiliate_event(
                        referrer_id, 
                        user_id, 
                        "NOVO_REFERENCIADO"
                    )
            else:
                await logger.log_system_event("ERRO", f"Falha ao adicionar usuário {user_id}")
        else:
            await logger.log_user_action(user_id, "RETORNO", "Usuário retornando")
        
        # Definir estado inicial
        context.user_data['state'] = UserStates.MAIN_MENU
        
        # Verificar se usuário já tem assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        
        # Enviar banner personalizado - SEMPRE TENTA IMAGEM PRIMEIRO
        banner_paths = [
            "banner.jpg",           # Raiz do projeto
            "banner.png", 
            "imperium_banner.jpg",
            "imperium_banner.png",
            "assets/banner.jpg",    # Pasta assets
            "assets/banner.png",
            "assets/imperium_banner.jpg",
            "assets/imperium_banner.png",
            "images/banner.jpg",    # Pasta images  
            "images/banner.png"
        ]
        
        banner_sent = False
        welcome_text = format_welcome_message(update.effective_user, subscription)
        keyboard = get_appropriate_keyboard(user_id)
        
        # Tentar enviar banner de qualquer um dos caminhos
        for banner_path in banner_paths:
            if os.path.exists(banner_path):
                try:
                    with open(banner_path, 'rb') as photo_file:
                        await update.message.reply_photo(
                            photo=photo_file,
                            caption=welcome_text,
                            reply_markup=keyboard,
                            parse_mode=ParseMode.HTML
                        )
                    banner_sent = True
                    logger.info(f"✅ Banner enviado: {banner_path}")
                    break
                except Exception as e:
                    logger.error(f"Erro ao enviar banner {banner_path}: {e}")
                    continue
        
        # Se não conseguiu enviar banner, enviar só texto
        if not banner_sent:
            await update.message.reply_text(
                welcome_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
            logger.info("📝 Banner não encontrado, enviado apenas texto")
        
        await logger.log_user_action(user_id, "START", "Comando /start executado")
        
    except Exception as e:
        logger.error(f"Erro no comando /start: {e}")
        await update.message.reply_text(
            "❌ Ocorreu um erro. Tente novamente em alguns instantes.",
            parse_mode=ParseMode.HTML
        )

def format_welcome_message(user, subscription: Optional[dict] = None) -> str:
    """
    Formata mensagem de boas-vindas personalizada
    
    Args:
        user: Objeto do usuário
        subscription: Dados da assinatura ativa (se houver)
    
    Returns:
        Mensagem formatada
    """
    try:
        name = get_user_display_name(user)
        
        if subscription:
            # Usuário com assinatura ativa
            end_date = subscription['end_date']
            if isinstance(end_date, str):
                from datetime import datetime
                end_date = datetime.fromisoformat(end_date)
            
            return f"""
✅ <b>Olá, {name}! Você já é membro do ᎥᗰᑭᗴᖇᎥᑌᗰ™!</b>

🎉 <b>Status:</b> Assinatura ativa
📅 <b>Válida até:</b> {format_date_br(end_date)}
🔑 <b>Acesso liberado a todas as ferramentas premium!</b>

🚀 <b>Links de acesso:</b>
• 📱 Grupo VIP: {VIP_GROUP_LINK}
• 🆘 Suporte: {SUPPORT_CONTACT}

💎 <b>Aproveite ao máximo sua assinatura!</b>

📱 <b>Use o menu abaixo para navegar:</b>
"""
        else:
            # Usuário sem assinatura
            return WELCOME_MESSAGE.format(name=name)
            
    except Exception as e:
        logger.error(f"Erro ao formatar mensagem de boas-vindas: {e}")
        return WELCOME_MESSAGE.format(name="amigo")

def get_appropriate_keyboard(user_id: int):
    """
    Retorna teclado apropriado baseado no tipo de usuário
    
    Args:
        user_id: ID do usuário
    
    Returns:
        Teclado inline apropriado
    """
    if user_id in ADMIN_IDS:
        return get_admin_menu_keyboard()
    else:
        return get_main_menu_keyboard()

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa callbacks do menu principal"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data == "main_menu":
            context.user_data['state'] = UserStates.MAIN_MENU
            
            # Verificar assinatura atual
            subscription = await db_manager.get_active_subscription(user_id)
            
            await query.edit_message_text(
                format_welcome_message(query.from_user, subscription),
                reply_markup=get_appropriate_keyboard(user_id),
                parse_mode=ParseMode.HTML
            )
            
            await logger.log_user_action(user_id, "MENU_PRINCIPAL", "Retorno ao menu")
        
        elif data == "my_subscription":
            await show_subscription_info(update, context)
        
        elif data == "affiliate_program":
            await show_affiliate_program(update, context)
        
        elif data == "support":
            await show_support_info(update, context)
        
    except Exception as e:
        logger.error(f"Erro no callback do menu: {e}")
        await query.answer("❌ Erro ao processar solicitação.")

async def show_subscription_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe informações da assinatura"""
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        subscription = await db_manager.get_active_subscription(user_id)
        
        if subscription:
            end_date = subscription['end_date']
            if isinstance(end_date, str):
                from datetime import datetime
                end_date = datetime.fromisoformat(end_date)
            
            plan_name = subscription.get('plan_name', 'N/A')
            
            info_message = f"""
📋 <b>INFORMAÇÕES DA ASSINATURA</b>

✅ <b>Status:</b> Ativa
💎 <b>Plano:</b> {plan_name}
📅 <b>Válida até:</b> {format_date_br(end_date)}

🚀 <b>Acesso liberado:</b>
• ✅ Todas as IAs premium
• ✅ Grupo VIP exclusivo
• ✅ Suporte prioritário
• ✅ Atualizações gratuitas

🔗 <b>Links importantes:</b>
• 📱 Grupo VIP: {VIP_GROUP_LINK}
• 🆘 Suporte: {SUPPORT_CONTACT}
"""
        else:
            info_message = """
❌ <b>NENHUMA ASSINATURA ATIVA</b>

🚫 Você não possui uma assinatura ativa no momento.

🛒 <b>Para ter acesso completo:</b>
• Adquira um de nossos planos
• Acesse todas as IAs premium
• Entre no grupo VIP exclusivo

💰 <b>Aproveite nossos preços promocionais!</b>
"""
        
        await query.edit_message_text(
            info_message,
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "CONSULTAR_ASSINATURA", "Informações visualizadas")
        
    except Exception as e:
        logger.error(f"Erro ao exibir informações da assinatura: {e}")
        await query.answer("❌ Erro ao carregar informações.")

async def show_affiliate_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe informações do programa de afiliados"""
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        # Buscar dados do afiliado
        affiliate_data = await db_manager.get_affiliate_stats(user_id)
        referrals_count = affiliate_data.get('total_referrals', 0)
        total_commission = affiliate_data.get('total_commission', 0.0)
        pending_commission = affiliate_data.get('pending_commission', 0.0)
        
        # Gerar link de afiliado
        affiliate_link = f"https://t.me/{context.bot.username}?start=ref_{user_id}"
        
        from config.settings import AFFILIATE_MESSAGE
        affiliate_info = f"""
{AFFILIATE_MESSAGE}

📊 <b>SEUS NÚMEROS:</b>
👥 <b>Referenciados:</b> {referrals_count}
💰 <b>Comissão total:</b> R$ {total_commission:.2f}
⏳ <b>Comissão pendente:</b> R$ {pending_commission:.2f}

🔗 <b>SEU LINK DE AFILIADO:</b>
<code>{affiliate_link}</code>

💡 <b>Como usar:</b>
1. Copie o link acima
2. Compartilhe em suas redes sociais
3. Ganhe 20% de cada venda realizada
4. Saque via Pix quando quiser

🎯 <b>Dica de ouro:</b> Conte para seus seguidores como as IAs estão revolucionando o mercado de trabalho!
"""
        
        await query.edit_message_text(
            affiliate_info,
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "PROGRAMA_AFILIADOS", "Informações acessadas")
        
    except Exception as e:
        logger.error(f"Erro ao exibir programa de afiliados: {e}")
        await query.answer("❌ Erro ao carregar informações de afiliados.")

async def show_support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe informações de suporte"""
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        support_message = f"""
🆘 <b>SUPORTE IMPERIUM™</b>

💬 <b>Precisa de ajuda? Estamos aqui para você!</b>

📞 <b>Canais de atendimento:</b>
• 💬 Suporte direto: {SUPPORT_CONTACT}
• ⚡ Resposta em até 2 horas
• 🕒 Atendimento 24h/7dias

❓ <b>Principais dúvidas:</b>
• ✅ Como acessar as ferramentas
• ✅ Problemas com pagamento
• ✅ Renovação de assinatura
• ✅ Dúvidas sobre afiliados

🔧 <b>Suporte técnico especializado</b>
Nossa equipe está sempre pronta para ajudar você a aproveitar ao máximo o Imperium™!

📱 <b>Clique no botão abaixo ou envie uma mensagem para:</b>
{SUPPORT_CONTACT}
"""
        
        await query.edit_message_text(
            support_message,
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "SUPORTE", "Informações acessadas")
        
    except Exception as e:
        logger.error(f"Erro ao exibir informações de suporte: {e}")
        await query.answer("❌ Erro ao carregar informações de suporte.")

def register_handlers(app: Application):
    """Registra todos os handlers do start"""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern="^(main_menu|my_subscription|affiliate_program|support)$"))