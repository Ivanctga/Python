"""
Handler para fluxo de pagamentos e Pix do Imperium™ Bot
Gerencia todo o processo de venda, desde seleção de plano até confirmação
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

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

router = Router()

@router.callback_query(F.data == "buy_plans")
async def show_plans(callback: CallbackQuery, state: FSMContext):
    """Exibe planos disponíveis"""
    try:
        user_id = callback.from_user.id
        
        # Verificar se já tem assinatura ativa
        subscription = await db_manager.get_active_subscription(user_id)
        if subscription:
            end_date = subscription['end_date']
            if isinstance(end_date, str):
                from datetime import datetime
                end_date = datetime.fromisoformat(end_date)
            
            await callback.message.edit_text(
                ERROR_MESSAGES["already_subscribed"].format(
                    end_date=format_date_br(end_date)
                ),
                reply_markup=get_main_menu_keyboard(),
                parse_mode="HTML"
            )
            await callback.answer()
            return
        
        await state.set_state(UserStates.SELECTING_PLAN)
        
        await callback.message.edit_text(
            BUY_MESSAGE,
            reply_markup=get_plans_keyboard(),
            parse_mode="HTML"
        )
        
        await callback.answer()
        await logger.log_user_action(user_id, "VISUALIZAR_PLANOS", "Tela de planos")
        
    except Exception as e:
        logger.error(f"Erro ao exibir planos: {e}")
        await callback.answer("❌ Erro ao carregar planos.")

@router.callback_query(F.data.startswith("select_plan:"))
async def select_plan(callback: CallbackQuery, state: FSMContext):
    """Processa seleção de plano"""
    try:
        user_id = callback.from_user.id
        plan_key = callback.data.split(":")[1]
        
        if plan_key not in PLANS:
            await callback.answer("❌ Plano inválido.")
            return
        
        plan = PLANS[plan_key]
        
        # Salvar plano selecionado no estado
        await state.update_data(selected_plan=plan_key)
        
        plan_details = f"""
🛒 <b>CONFIRMAR COMPRA</b>

{plan['emoji']} <b>Plano Selecionado:</b> {plan['name']}
💰 <b>Valor:</b> {format_currency(plan['price'])}
📅 <b>Duração:</b> {plan['duration_days']} dias
📝 <b>Descrição:</b>
{plan['description']}

💎 <b>O que está incluso:</b>
• ✅ Acesso completo ao Imperium™
• ✅ Grupo VIP exclusivo
• ✅ Downloads ilimitados
• ✅ Atualizações constantes
• ✅ Suporte premium

🔄 Confirme para continuar com a compra:
"""
        
        await callback.message.edit_text(
            plan_details,
            reply_markup=get_plan_confirmation_keyboard(plan_key),
            parse_mode="HTML"
        )
        
        await callback.answer()
        await logger.log_user_action(user_id, "SELECIONAR_PLANO", f"Plano: {plan['name']}")
        
    except Exception as e:
        logger.error(f"Erro ao selecionar plano: {e}")
        await callback.answer("❌ Erro ao selecionar plano.")

@router.callback_query(F.data.startswith("confirm_plan:"))
async def confirm_plan(callback: CallbackQuery, state: FSMContext):
    """Confirma plano e solicita telefone"""
    try:
        user_id = callback.from_user.id
        plan_key = callback.data.split(":")[1]
        
        if plan_key not in PLANS:
            await callback.answer("❌ Plano inválido.")
            return
        
        await state.set_state(UserStates.ENTERING_PHONE)
        await state.update_data(selected_plan=plan_key)
        
        phone_message = """
📱 <b>INFORMAR TELEFONE</b>

Para continuar com sua compra, preciso do seu número de telefone para contato.

📝 <b>Digite apenas os números:</b>
• Exemplo: 11999887766
• Não usar parênteses, traços ou espaços
• Incluir o DDD

🔒 <b>Seus dados estão seguros conosco!</b>
"""
        
        await callback.message.edit_text(
            phone_message,
            reply_markup=get_cancel_keyboard(),
            parse_mode="HTML"
        )
        
        await callback.answer()
        await logger.log_user_action(user_id, "CONFIRMAR_PLANO", f"Plano: {plan_key}")
        
    except Exception as e:
        logger.error(f"Erro ao confirmar plano: {e}")
        await callback.answer("❌ Erro ao confirmar plano.")

@router.message(UserStates.ENTERING_PHONE)
async def process_phone(message: Message, state: FSMContext):
    """Processa telefone informado"""
    try:
        user_id = message.from_user.id
        phone_text = message.text.strip()
        
        # Validar telefone
        is_valid, result = validate_phone(phone_text)
        
        if not is_valid:
            await message.answer(
                ERROR_MESSAGES["invalid_phone"],
                reply_markup=get_cancel_keyboard(),
                parse_mode="HTML"
            )
            return
        
        # Salvar telefone no banco e no estado
        await db_manager.update_user_phone(user_id, result)
        await state.update_data(phone=result)
        
        # Gerar pagamento
        await generate_payment(message, state)
        
        await logger.log_user_action(user_id, "TELEFONE_INFORMADO", f"Telefone validado")
        
    except Exception as e:
        logger.error(f"Erro ao processar telefone: {e}")
        await message.answer(
            "❌ Erro ao processar telefone. Tente novamente.",
            reply_markup=get_cancel_keyboard()
        )

async def generate_payment(message: Message, state: FSMContext):
    """Gera pagamento Pix"""
    try:
        user_id = message.from_user.id
        state_data = await state.get_data()
        
        plan_key = state_data.get('selected_plan')
        phone = state_data.get('phone')
        
        if not plan_key or plan_key not in PLANS:
            await message.answer("❌ Erro: plano não encontrado.")
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
            await message.answer(
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
        
        await state.set_state(PaymentStates.WAITING_PAYMENT)
        await state.update_data(payment_id=payment_data['id'])
        
        if qr_image_bytes:
            # Enviar QR Code como foto
            photo = BufferedInputFile(qr_image_bytes, filename="qr_code.png")
            await message.answer_photo(
                photo=photo,
                caption=payment_message,
                reply_markup=get_payment_keyboard(payment_data['id']),
                parse_mode="HTML"
            )
        else:
            # Fallback apenas texto
            await message.answer(
                payment_message,
                reply_markup=get_payment_keyboard(payment_data['id']),
                parse_mode="HTML"
            )
        
        await logger.log_payment_event(
            user_id, payment_data['id'], "GERADO", plan['price']
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar pagamento: {e}")
        await message.answer(
            ERROR_MESSAGES["payment_error"],
            reply_markup=get_main_menu_keyboard()
        )

@router.callback_query(F.data.startswith("check_payment:"))
async def check_payment(callback: CallbackQuery, state: FSMContext):
    """Verifica status do pagamento"""
    try:
        user_id = callback.from_user.id
        payment_id = callback.data.split(":")[1]
        
        # Verificar status no Mercado Pago
        payment_info = mp_payment.get_payment_info(payment_id)
        
        if not payment_info:
            await callback.answer("❌ Erro ao verificar pagamento.")
            return
        
        # Atualizar status no banco
        await db_manager.update_payment_status(payment_id, payment_info['status'])
        
        if payment_info['is_approved']:
            await process_approved_payment(callback, state, payment_id)
        elif payment_info['is_expired']:
            await process_expired_payment(callback, state, payment_id)
        else:
            await process_pending_payment(callback, payment_info)
        
        await logger.log_payment_event(
            user_id, payment_id, f"VERIFICADO_{payment_info['status'].upper()}"
        )
        
    except Exception as e:
        logger.error(f"Erro ao verificar pagamento: {e}")
        await callback.answer("❌ Erro ao verificar pagamento.")

async def process_approved_payment(callback: CallbackQuery, state: FSMContext, payment_id: str):
    """Processa pagamento aprovado"""
    try:
        user_id = callback.from_user.id
        state_data = await state.get_data()
        plan_key = state_data.get('selected_plan')
        
        if not plan_key or plan_key not in PLANS:
            await callback.answer("❌ Erro: dados do plano não encontrados.")
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
            await callback.answer("❌ Erro ao criar assinatura.")
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
        
        success_msg = SUCCESS_MESSAGE.format(
            vip_group_link=VIP_GROUP_LINK,
            end_date=format_date_br(end_date),
            support_contact=SUPPORT_CONTACT
        )
        
        await state.set_state(UserStates.PAYMENT_CONFIRMED)
        
        await callback.message.edit_text(
            success_msg,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        
        await callback.answer("🎉 Pagamento aprovado!")
        await logger.log_payment_event(user_id, payment_id, "APROVADO", plan['price'])
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento aprovado: {e}")
        await callback.answer("❌ Erro ao processar pagamento.")

async def process_pending_payment(callback: CallbackQuery, payment_info: dict):
    """Processa pagamento pendente"""
    try:
        pending_msg = PAYMENT_PENDING_MESSAGE.format(
            time_remaining=payment_info['time_remaining'],
            support_contact=SUPPORT_CONTACT
        )
        
        await callback.message.edit_text(
            pending_msg,
            reply_markup=get_payment_keyboard(payment_info['id']),
            parse_mode="HTML"
        )
        
        await callback.answer("⏳ Pagamento ainda pendente...")
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento pendente: {e}")
        await callback.answer("❌ Erro ao atualizar status.")

async def process_expired_payment(callback: CallbackQuery, state: FSMContext, payment_id: str):
    """Processa pagamento expirado"""
    try:
        expired_msg = PAYMENT_EXPIRED_MESSAGE.format(
            support_contact=SUPPORT_CONTACT
        )
        
        await state.set_state(UserStates.MAIN_MENU)
        
        await callback.message.edit_text(
            expired_msg,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        
        await callback.answer("⌛ Pagamento expirado.")
        await logger.log_payment_event(
            callback.from_user.id, payment_id, "EXPIRADO"
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar pagamento expirado: {e}")
        await callback.answer("❌ Erro ao processar expiração.")

@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    """Cancela pagamento atual"""
    try:
        user_id = callback.from_user.id
        
        await state.set_state(UserStates.MAIN_MENU)
        await state.clear()
        
        await callback.message.edit_text(
            "❌ <b>Pagamento cancelado</b>\n\nVocê pode iniciar uma nova compra a qualquer momento.",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        
        await callback.answer("❌ Pagamento cancelado.")
        await logger.log_user_action(user_id, "CANCELAR_PAGAMENTO", "Usuario cancelou")
        
    except Exception as e:
        logger.error(f"Erro ao cancelar pagamento: {e}")
        await callback.answer("❌ Erro ao cancelar.")