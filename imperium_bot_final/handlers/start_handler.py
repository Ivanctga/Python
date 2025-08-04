"""
Handler para comando /start e fluxo inicial do Imperium™ Bot
Gerencia entrada de usuários, referências e menu principal
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from typing import Optional

from database.models import db_manager
from states.user_states import UserStates
from keyboards.inline_keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from config.settings import (
    WELCOME_MESSAGE, ADMIN_IDS, VIP_GROUP_LINK, 
    SUPPORT_CONTACT, format_date_br
)
from utils.helpers import extract_referrer_from_start, get_user_display_name
from utils.logger import logger
import os

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext, command: CommandStart):
    """
    Processa comando /start com ou sem parâmetros de referência
    
    Args:
        message: Mensagem do usuário
        state: Estado FSM
        command: Objeto do comando start
    """
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        
        # Extrair referenciador se houver
        referrer_id = None
        start_param = command.args
        
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
        await state.set_state(UserStates.MAIN_MENU)
        
        # Verificar se usuário já tem assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        
        # Enviar banner se existir
        banner_path = "assets/imperium_banner.jpg"
        if os.path.exists(banner_path):
            try:
                photo = FSInputFile(banner_path)
                await message.answer_photo(
                    photo=photo,
                    caption=format_welcome_message(message.from_user, subscription),
                    reply_markup=get_appropriate_keyboard(user_id),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Erro ao enviar banner: {e}")
                # Fallback sem imagem
                await send_text_welcome(message, subscription, user_id)
        else:
            await send_text_welcome(message, subscription, user_id)
        
    except Exception as e:
        logger.error(f"Erro no comando /start para usuário {user_id}: {e}")
        await message.answer(
            "❌ Ocorreu um erro ao iniciar. Tente novamente em alguns instantes.",
            reply_markup=get_main_menu_keyboard()
        )

@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    """
    Comando administrativo
    
    Args:
        message: Mensagem do usuário
        state: Estado FSM
    """
    try:
        user_id = message.from_user.id
        
        # Verificar se é administrador
        if user_id not in ADMIN_IDS:
            await message.answer("❌ Acesso negado. Apenas administradores podem usar este comando.")
            await logger.log_user_action(user_id, "TENTATIVA_ACESSO_ADMIN", "Acesso negado")
            return
        
        # Definir estado administrativo
        await state.set_state(UserStates.ADMIN_MENU)
        
        # Buscar estatísticas básicas
        stats = await db_manager.get_statistics()
        
        admin_message = f"""
🔐 <b>PAINEL ADMINISTRATIVO - IMPERIUM™</b>

👋 Bem-vindo, {get_user_display_name(message.from_user.__dict__)}!

📊 <b>Estatísticas Rápidas:</b>
👥 Usuários: <b>{stats.get('total_users', 0)}</b>
🆕 Novos hoje: <b>{stats.get('users_today', 0)}</b>
💎 Assinaturas ativas: <b>{stats.get('active_subscriptions', 0)}</b>
💰 Faturamento total: <b>R$ {stats.get('total_revenue', 0):.2f}</b>
💸 Saques pendentes: <b>{stats.get('pending_withdrawals', 0)}</b>

🎯 Escolha uma opção abaixo:
"""
        
        await message.answer(
            admin_message,
            reply_markup=get_admin_menu_keyboard(),
            parse_mode="HTML"
        )
        
        await logger.log_admin_action(user_id, "ACESSO_PAINEL", "Dashboard")
        
    except Exception as e:
        logger.error(f"Erro no comando /admin para usuário {user_id}: {e}")
        await message.answer("❌ Erro ao acessar painel administrativo.")

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """
    Retorna ao menu principal
    
    Args:
        callback: Callback query
        state: Estado FSM
    """
    try:
        user_id = callback.from_user.id
        
        # Limpar estado e voltar ao menu principal
        await state.set_state(UserStates.MAIN_MENU)
        
        # Verificar assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        
        welcome_msg = format_welcome_message(callback.from_user, subscription)
        
        await callback.message.edit_text(
            welcome_msg,
            reply_markup=get_appropriate_keyboard(user_id),
            parse_mode="HTML"
        )
        
        await callback.answer("🏠 Voltando ao menu principal...")
        await logger.log_user_action(user_id, "VOLTAR_MENU", "Menu principal")
        
    except Exception as e:
        logger.error(f"Erro ao voltar ao menu principal: {e}")
        await callback.answer("❌ Erro ao voltar ao menu.")

@router.message(Command("menu"))
async def menu_command(message: Message, state: FSMContext):
    """
    Comando para acessar menu principal
    
    Args:
        message: Mensagem do usuário
        state: Estado FSM
    """
    try:
        user_id = message.from_user.id
        
        await state.set_state(UserStates.MAIN_MENU)
        
        subscription = await db_manager.get_active_subscription(user_id)
        welcome_msg = format_welcome_message(message.from_user, subscription)
        
        await message.answer(
            welcome_msg,
            reply_markup=get_appropriate_keyboard(user_id),
            parse_mode="HTML"
        )
        
        await logger.log_user_action(user_id, "COMANDO_MENU", "Acesso via comando")
        
    except Exception as e:
        logger.error(f"Erro no comando /menu: {e}")
        await message.answer("❌ Erro ao carregar menu.")

@router.message(Command("status"))
async def status_command(message: Message):
    """
    Comando para verificar status da assinatura
    
    Args:
        message: Mensagem do usuário
    """
    try:
        user_id = message.from_user.id
        
        # Buscar assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        
        if subscription:
            end_date = subscription['end_date']
            if isinstance(end_date, str):
                from datetime import datetime
                end_date = datetime.fromisoformat(end_date)
            
            status_msg = f"""
✅ <b>ASSINATURA ATIVA</b>

💎 <b>Plano:</b> {subscription['plan_name']}
💰 <b>Valor pago:</b> R$ {subscription['plan_price']:.2f}
📅 <b>Válida até:</b> {format_date_br(end_date)}
🎮 <b>Status:</b> Acesso liberado

🔗 <b>Acesso ao grupo VIP:</b>
{VIP_GROUP_LINK}

🆘 <b>Suporte:</b> {SUPPORT_CONTACT}
"""
        else:
            status_msg = f"""
❌ <b>NENHUMA ASSINATURA ATIVA</b>

😔 Você não possui uma assinatura ativa no momento.

🛒 Para adquirir o Imperium™, use: /start
👥 Para se tornar afiliado, use: /start

🆘 <b>Precisa de ajuda?</b> {SUPPORT_CONTACT}
"""
        
        await message.answer(status_msg, parse_mode="HTML")
        await logger.log_user_action(user_id, "VERIFICAR_STATUS", "Comando /status")
        
    except Exception as e:
        logger.error(f"Erro no comando /status: {e}")
        await message.answer("❌ Erro ao verificar status da assinatura.")

def format_welcome_message(user, subscription: Optional[dict]) -> str:
    """
    Formata mensagem de boas-vindas personalizada
    
    Args:
        user: Objeto do usuário
        subscription: Dados da assinatura (se houver)
    
    Returns:
        Mensagem formatada
    """
    from utils.helpers import get_greeting
    
    greeting = get_greeting()
    name = get_user_display_name(user.__dict__)
    
    base_message = f"{greeting}, {name}!\n\n{WELCOME_MESSAGE}"
    
    if subscription:
        end_date = subscription['end_date']
        if isinstance(end_date, str):
            from datetime import datetime
            end_date = datetime.fromisoformat(end_date)
        
        base_message += f"""

✅ <b>SUA ASSINATURA ESTÁ ATIVA!</b>
💎 Plano: {subscription['plan_name']}
📅 Válida até: {format_date_br(end_date)}

🎮 <b>Acesso liberado ao grupo VIP:</b>
{VIP_GROUP_LINK}
"""
    
    return base_message

def get_appropriate_keyboard(user_id: int):
    """
    Retorna teclado apropriado baseado no tipo de usuário
    
    Args:
        user_id: ID do usuário
    
    Returns:
        Teclado apropriado
    """
    if user_id in ADMIN_IDS:
        # Adicionar botão de admin para administradores
        from keyboards.inline_keyboards import InlineKeyboardBuilder, InlineKeyboardButton
        from config.settings import EMOJIS
        
        builder = InlineKeyboardBuilder()
        
        # Botões normais do menu principal
        builder.row(
            InlineKeyboardButton(
                text=f"{EMOJIS['cart']} QUERO ADQUIRIR O IMPERIUM™",
                callback_data="buy_plans"
            )
        )
        
        builder.row(
            InlineKeyboardButton(
                text=f"{EMOJIS['users']} SISTEMA DE AFILIADOS",
                callback_data="affiliate_menu"
            )
        )
        
        # Botão administrativo
        builder.row(
            InlineKeyboardButton(
                text=f"{EMOJIS['gear']} PAINEL ADMINISTRATIVO",
                callback_data="admin_menu"
            )
        )
        
        # Suporte e canal
        builder.row(
            InlineKeyboardButton(
                text=f"{EMOJIS['info']} SUPORTE",
                url="https://t.me/seu_suporte"
            ),
            InlineKeyboardButton(
                text=f"{EMOJIS['rocket']} CANAL",
                url="https://t.me/seu_canal"
            )
        )
        
        return builder.as_markup()
    else:
        return get_main_menu_keyboard()

async def send_text_welcome(message: Message, subscription: Optional[dict], user_id: int):
    """
    Envia mensagem de boas-vindas apenas texto
    
    Args:
        message: Mensagem original
        subscription: Dados da assinatura
        user_id: ID do usuário
    """
    welcome_msg = format_welcome_message(message.from_user, subscription)
    
    await message.answer(
        welcome_msg,
        reply_markup=get_appropriate_keyboard(user_id),
        parse_mode="HTML"
    )

@router.message(Command("help"))
async def help_command(message: Message):
    """
    Comando de ajuda
    
    Args:
        message: Mensagem do usuário
    """
    help_text = f"""
🆘 <b>AJUDA - IMPERIUM™ BOT</b>

📋 <b>Comandos disponíveis:</b>
/start - Iniciar o bot
/menu - Acessar menu principal
/status - Verificar status da assinatura
/help - Esta mensagem de ajuda

🛒 <b>Para comprar:</b>
1. Use /start
2. Clique em "QUERO ADQUIRIR O IMPERIUM™"
3. Escolha seu plano
4. Informe seu telefone
5. Pague via Pix

👥 <b>Para ser afiliado:</b>
1. Use /start
2. Clique em "SISTEMA DE AFILIADOS"
3. Gere seu link de afiliado
4. Compartilhe e ganhe 20% de comissão

🆘 <b>Suporte:</b> {SUPPORT_CONTACT}
📢 <b>Canal:</b> https://t.me/seu_canal
"""
    
    await message.answer(help_text, parse_mode="HTML")

# Fallback para mensagens não reconhecidas
@router.message()
async def unknown_message(message: Message, state: FSMContext):
    """
    Handler para mensagens não reconhecidas
    
    Args:
        message: Mensagem do usuário
        state: Estado FSM
    """
    try:
        user_id = message.from_user.id
        current_state = await state.get_state()
        
        # Se não está em nenhum estado específico, redirecionar para menu
        if not current_state or current_state == UserStates.MAIN_MENU:
            await message.answer(
                "🤔 Não entendi sua mensagem. Use os botões abaixo para navegar:",
                reply_markup=get_appropriate_keyboard(user_id)
            )
        else:
            # Está em algum fluxo específico, dar dica
            await message.answer(
                "📝 Por favor, use os botões disponíveis ou cancele a operação atual.",
                reply_markup=get_main_menu_keyboard()
            )
        
        await logger.log_user_action(user_id, "MENSAGEM_NAO_RECONHECIDA", message.text[:100])
        
    except Exception as e:
        logger.error(f"Erro no handler de mensagem desconhecida: {e}")
        await message.answer("❌ Erro ao processar mensagem.")