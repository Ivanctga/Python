"""
Handler para fluxo de pagamentos e Pix do Imperium™ Bot
Gerencia todo o processo de venda, desde seleção de plano até confirmação
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from database.models import db_manager
from states.user_states import UserStates, PaymentStates
from keyboards.inline_keyboards import (
    get_plans_keyboard, get_plan_confirmation_keyboard, 
    get_payment_keyboard, get_cancel_keyboard, get_main_menu_keyboard
)
from config.settings import (
    PLANS, BUY_MESSAGE, PAYMENT_INSTRUCTIONS, SUCCESS_MESSAGE,
    PAYMENT_PENDING_MESSAGE, PAYMENT_EXPIRED_MESSAGE, ERROR_MESSAGES,
    VIP_GROUP_LINK, SUPPORT_CONTACT, COMMISSION_RATE, format_currency
)
from utils.helpers import validate_phone, format_date_br, calculate_commission
from utils.logger import logger
from payments.mercado_pago import mp_payment
from payments.qr_generator import qr_generator

async def show_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe planos disponíveis"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Verificar se já tem assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        if subscription:
            end_date = subscription['end_date']
            if isinstance(end_date, str):
                from datetime import datetime
                end_date = datetime.fromisoformat(end_date)
            
            await query.edit_message_text(
                ERROR_MESSAGES["already_subscribed"].format(
                    end_date=format_date_br(end_date)
                ),
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Salvar estado no context
        context.user_data['state'] = UserStates.SELECTING_PLAN
        
        await query.edit_message_text(
            BUY_MESSAGE,
            reply_markup=get_plans_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "VISUALIZAR_PLANOS", "Tela de planos")
        
    except Exception as e:
        logger.error(f"Erro ao exibir planos: {e}")
        await query.answer("❌ Erro ao carregar planos.")

async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa seleção de plano"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        plan_key = query.data.split(":")[1]
        
        if plan_key not in PLANS:
            await query.answer("❌ Plano inválido.")
            return
        
        plan = PLANS[plan_key]
        
        # Salvar plano selecionado no context
        context.user_data['selected_plan'] = plan_key
        
        plan_details = f"""
🛒 <b>CONFIRMAR COMPRA</b>

{plan['emoji']} <b>Plano Selecionado:</b> {plan['name']}
💰 <b>Valor:</b> {format_currency(plan['price'])}
📅 <b>Duração:</b> {plan['duration_days']} dias
📝 <b>Descrição:</b>
{plan['description']}

🤖 <b>O que está incluso:</b>
• ✅ Acesso a todas as IAs premium
• ✅ Grupo VIP exclusivo
• ✅ Plataforma completa de ferramentas
• ✅ Atualizações constantes
• ✅ Suporte premium

🔄 Confirme para continuar com a compra:
"""
        
        await query.edit_message_text(
            plan_details,
            reply_markup=get_plan_confirmation_keyboard(plan_key),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "SELECIONAR_PLANO", f"Plano: {plan['name']}")
        
    except Exception as e:
        logger.error(f"Erro ao selecionar plano: {e}")
        await query.answer("❌ Erro ao selecionar plano.")

async def confirm_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirma plano e solicita telefone"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        plan_key = query.data.split(":")[1]
        
        if plan_key not in PLANS:
            await query.answer("❌ Plano inválido.")
            return
        
        context.user_data['state'] = UserStates.ENTERING_PHONE
        context.user_data['selected_plan'] = plan_key
        
        phone_message = """
📱 <b>INFORMAR TELEFONE</b>

Para continuar com sua compra, preciso do seu número de telefone para contato.

📝 <b>Digite apenas os números:</b>
• Exemplo: 11999887766
• Não usar parênteses, traços ou espaços
• Incluir o DDD

🔒 <b>Seus dados estão seguros conosco!</b>
"""
        
        await query.edit_message_text(
            phone_message,
            reply_markup=get_cancel_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await logger.log_user_action(user_id, "CONFIRMAR_PLANO", f"Plano: {plan_key}")
        
    except Exception as e:
        logger.error(f"Erro ao confirmar plano: {e}")
        await query.answer("❌ Erro ao confirmar plano.")

async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa telefone informado"""
    try:
        user_id = update.effective_user.id
        phone_text = update.message.text.strip()
        
        # Verificar se está no estado correto
        if context.user_data.get('state') != UserStates.ENTERING_PHONE:
            return
        
        # Validar telefone
        is_valid, result = validate_phone(phone_text)
        
        if not is_valid:
            await update.message.reply_text(
                ERROR_MESSAGES["invalid_phone"],
                reply_markup=get_cancel_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Salvar telefone no banco e no context
        await db_manager.update_user_phone(user_id, result)
        context.user_data['phone'] = result
        
        # Gerar pagamento
        await generate_payment(update, context)
        
        await logger.log_user_action(user_id, "TELEFONE_INFORMADO", f"Telefone validado")
        
    except Exception as e:
        logger.error(f"Erro ao processar telefone: {e}")
        await update.message.reply_text(
            "❌ Erro ao processar telefone. Tente novamente.",
            reply_markup=get_cancel_keyboard()
        )

async def generate_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera pagamento Pix"""
    try:
        user_id = update.effective_user.id
        
        plan_key = context.user_data.get('selected_plan')
        phone = context.user_data.get('phone')
        
        if not plan_key or plan_key not in PLANS:
            await update.message.reply_text("❌ Erro: plano não encontrado.")
            return
        
        plan = PLANS[plan_key]
        
        # Criar pagamento no Mercado Pago
        payment_data = mp_payment.create_pix_payment(
            user_id=user_id,
            user_phone=phone,
            amount=plan['price'],
            plan_name=plan['name'],
            description=f"Imperium™ - Plano {plan['name']}"
        )
        
        if not payment_data:
            await update.message.reply_text(
                ERROR_MESSAGES["payment_error"],
                reply_markup=get_main_menu_keyboard()
            )
            return
        
        # Salvar pagamento no banco
        await db_manager.create_payment(
            user_id=user_id,
            mp_payment_id=payment_data['id'],
            amount=plan['price'],
            plan_name=plan['name'],
            qr_code_data=payment_data['qr_code_data'],
            qr_code_base64=payment_data.get('qr_code_base64', '')
        )
        
        # Gerar QR Code com informações
        qr_image_bytes = qr_generator.generate_qr_with_info(
            payment_data['qr_code_data'],
            plan['price'],
            f"Imperium™ - {plan['name']}"
        )
        
        # Mensagem de pagamento
        payment_message = f"""
💳 <b>PAGAMENTO PIX GERADO</b>

{plan['emoji']} <b>Plano:</b> {plan['name']}
💰 <b>Valor:</b> {format_currency(plan['price'])}
🆔 <b>ID:</b> <code>{payment_data['id']}</code>

{PAYMENT_INSTRUCTIONS.format(support_contact=SUPPORT_CONTACT)}

📋 <b>Código Pix (Copia e Cola):</b>
<code>{payment_data['qr_code_data']}</code>

⏰ <b>Este Pix expira em 24 horas!</b>
"""
        
        context.user_data['state'] = PaymentStates.WAITING_PAYMENT
        context.user_data['payment_id'] = payment_data['id']
        
        if qr_image_bytes:
            # Enviar QR Code como foto
            await update.message.reply_photo(
                photo=qr_image_bytes,
                caption=payment_message,
                reply_markup=get_payment_keyboard(payment_data['id']),
                parse_mode=ParseMode.HTML
            )
        else:
            # Fallback apenas texto
            await update.message.reply_text(
                payment_message,
                reply_markup=get_payment_keyboard(payment_data['id']),
                parse_mode=ParseMode.HTML
            )
        
        await logger.log_payment_event(
            user_id, payment_data['id'], "GERADO", plan['price']
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar pagamento: {e}")
        await update.message.reply_text(
            ERROR_MESSAGES["payment_error"],
            reply_markup=get_main_menu_keyboard()
        )

async def check_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica status do pagamento"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        payment_id = query.data.split(":")[1]
        
        # Verificar status no Mercado Pago
        payment_info = mp_payment.get_payment_info(payment_id)
        
        if not payment_info:
            await query.answer("❌ Erro ao verificar pagamento.")
            return
        
        # Atualizar status no banco
        await db_manager.update_payment_status(payment_id, payment_info['status'])
        
        if payment_info['is_approved']:
            await process_approved_payment(update, context, payment_id)
        elif payment_info['is_expired']:
            await process_expired_payment(update, context, payment_id)
        else:
            await process_pending_payment(update, payment_info)
        
        await logger.log_payment_event(
            user_id, payment_id, f"VERIFICADO_{payment_info['status'].upper()}"
        )
        
    except Exception as e:
        logger.error(f"Erro ao verificar pagamento: {e}")
        await query.answer("❌ Erro ao verificar pagamento.")

async def process_approved_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, payment_id: str):
    """Processa pagamento aprovado"""
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        plan_key = context.user_data.get('selected_plan')
        
        if not plan_key or plan_key not in PLANS:
            await query.answer("❌ Erro: dados do plano não encontrados.")
            return
        
        plan = PLANS[plan_key]
        
        # Criar assinatura
        subscription_id = await db_manager.create_subscription(
            user_id=user_id,
            plan_name=plan['name'],
            plan_price=plan['price'],
            duration_days=plan['duration_days'],
            payment_id=payment_id
        )
        
        if not subscription_id:
            await query.answer("❌ Erro ao criar assinatura.")
            return
        
        # Processar comissão de afiliado se houver
        user_data = await db_manager.get_user(user_id)
        if user_data and user_data.get('referrer_id'):
            commission = calculate_commission(plan['price'], COMMISSION_RATE)
            await db_manager.create_affiliate_sale(
                affiliate_id=user_data['referrer_id'],
                referred_user_id=user_id,
                subscription_id=subscription_id,
                commission_amount=commission
            )
            
            await logger.log_affiliate_event(
                user_data['referrer_id'], user_id, "NOVA_VENDA", commission
            )
        
        # Calcular data de vencimento
        from datetime import datetime, timedelta
        end_date = datetime.now() + timedelta(days=plan['duration_days'])
        
        # Gerar link único para o grupo VIP
        unique_invite_link = await generate_unique_invite_link(context.bot, user_id)
        
        success_msg = SUCCESS_MESSAGE.format(
            vip_group_link=unique_invite_link,
            end_date=format_date_br(end_date),
            support_contact=SUPPORT_CONTACT
        )
        
        context.user_data['state'] = UserStates.PAYMENT_CONFIRMED
        
        await query.edit_message_text(
            success_msg,
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await query.answer("🎉 Pagamento aprovado!")
        await logger.log_payment_event(user_id, payment_id, "APROVADO", plan['price'])
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento aprovado: {e}")
        await query.answer("❌ Erro ao processar pagamento.")

async def generate_unique_invite_link(bot, user_id: int) -> str:
    """
    Gera um link de convite único para o grupo VIP que só funciona para o usuário específico
    """
    try:
        # Extrair chat_id do VIP_GROUP_LINK
        # Assumindo que VIP_GROUP_LINK está no formato https://t.me/grupo_vip
        # Vou implementar uma versão que cria um convite de uso único
        
        group_username = VIP_GROUP_LINK.split('/')[-1]
        
        # Criar um invite link de uso único
        invite_link = await bot.create_chat_invite_link(
            chat_id=f"@{group_username}",
            member_limit=1,  # Apenas 1 pessoa pode usar
            name=f"Convite_Usuario_{user_id}"
        )
        
        logger.info(f"Link único criado para usuário {user_id}: {invite_link.invite_link}")
        return invite_link.invite_link
        
    except Exception as e:
        logger.error(f"Erro ao gerar link único: {e}")
        # Fallback para o link padrão se não conseguir criar o link único
        return VIP_GROUP_LINK

async def process_pending_payment(update: Update, payment_info: dict):
    """Processa pagamento pendente"""
    try:
        query = update.callback_query
        
        pending_msg = PAYMENT_PENDING_MESSAGE.format(
            time_remaining=payment_info['time_remaining'],
            support_contact=SUPPORT_CONTACT
        )
        
        await query.edit_message_text(
            pending_msg,
            reply_markup=get_payment_keyboard(payment_info['id']),
            parse_mode=ParseMode.HTML
        )
        
        await query.answer("⏳ Pagamento ainda pendente...")
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento pendente: {e}")
        await query.answer("❌ Erro ao atualizar status.")

async def process_expired_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, payment_id: str):
    """Processa pagamento expirado"""
    try:
        query = update.callback_query
        
        expired_msg = PAYMENT_EXPIRED_MESSAGE.format(
            support_contact=SUPPORT_CONTACT
        )
        
        context.user_data['state'] = UserStates.MAIN_MENU
        
        await query.edit_message_text(
            expired_msg,
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await query.answer("⌛ Pagamento expirado.")
        await logger.log_payment_event(
            query.from_user.id, payment_id, "EXPIRADO"
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento expirado: {e}")
        await query.answer("❌ Erro ao processar expiração.")

async def cancel_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela pagamento atual"""
    try:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        context.user_data['state'] = UserStates.MAIN_MENU
        context.user_data.clear()
        
        await query.edit_message_text(
            "❌ <b>Pagamento cancelado</b>\n\nVocê pode iniciar uma nova compra a qualquer momento.",
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )
        
        await query.answer("❌ Pagamento cancelado.")
        await logger.log_user_action(user_id, "CANCELAR_PAGAMENTO", "Usuario cancelou")
        
    except Exception as e:
        logger.error(f"Erro ao cancelar pagamento: {e}")
        await query.answer("❌ Erro ao cancelar.")

def register_handlers(app: Application):
    """Registra todos os handlers de pagamento"""
    app.add_handler(CallbackQueryHandler(show_plans, pattern="^buy_plans$"))
    app.add_handler(CallbackQueryHandler(select_plan, pattern="^select_plan:"))
    app.add_handler(CallbackQueryHandler(confirm_plan, pattern="^confirm_plan:"))
    app.add_handler(CallbackQueryHandler(check_payment, pattern="^check_payment:"))
    app.add_handler(CallbackQueryHandler(cancel_payment, pattern="^cancel_payment$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_phone))