"""
Teclados inline para o Imperium™ Bot
Define todos os botões e menus utilizados na interface
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Optional
from config.settings import PLANS, format_currency, EMOJIS

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu principal
    
    Returns:
        Teclado inline do menu principal
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['cart']} QUERO ADQUIRIR O IMPERIUM™", callback_data="buy_plans")],
        [InlineKeyboardButton(f"{EMOJIS['users']} SISTEMA DE AFILIADOS", callback_data="affiliate_program")],
        [InlineKeyboardButton(f"{EMOJIS['diamond']} MINHA ASSINATURA", callback_data="my_subscription")],
        [
            InlineKeyboardButton(f"{EMOJIS['info']} SUPORTE", callback_data="support"),
            InlineKeyboardButton(f"{EMOJIS['rocket']} CANAL", url="https://t.me/seu_canal")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_plans_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado com planos disponíveis
    
    Returns:
        Teclado inline com planos
    """
    keyboard = []
    
    # Adicionar cada plano
    for plan_key, plan_data in PLANS.items():
        button_text = f"{plan_data['emoji']} {plan_data['name']} - {format_currency(plan_data['price'])}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"select_plan:{plan_key}")])
    
    # Botão voltar
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['cross']} VOLTAR AO MENU", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_plan_confirmation_keyboard(plan_key: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado de confirmação do plano
    
    Args:
        plan_key: Chave do plano selecionado
    
    Returns:
        Teclado de confirmação
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['check']} CONFIRMAR COMPRA", callback_data=f"confirm_plan:{plan_key}")],
        [InlineKeyboardButton(f"{EMOJIS['cross']} VOLTAR AOS PLANOS", callback_data="buy_plans")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard(payment_id: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado para pagamento
    
    Args:
        payment_id: ID do pagamento
    
    Returns:
        Teclado de pagamento
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['check']} VERIFICAR PAGAMENTO", callback_data=f"check_payment:{payment_id}")],
        [InlineKeyboardButton(f"{EMOJIS['cross']} CANCELAR", callback_data="cancel_payment")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_affiliate_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu de afiliados
    
    Returns:
        Teclado do menu de afiliados
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['target']} MEU DASHBOARD", callback_data="affiliate_dashboard")],
        [InlineKeyboardButton(f"{EMOJIS['rocket']} MEU LINK DE AFILIADO", callback_data="my_affiliate_link")],
        [InlineKeyboardButton(f"{EMOJIS['money']} SOLICITAR SAQUE", callback_data="request_withdrawal")],
        [InlineKeyboardButton(f"{EMOJIS['book']} HISTÓRICO DE VENDAS", callback_data="sales_history")],
        [InlineKeyboardButton(f"{EMOJIS['cross']} VOLTAR AO MENU", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu administrativo
    
    Returns:
        Teclado administrativo
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['target']} DASHBOARD", callback_data="admin_dashboard")],
        [
            InlineKeyboardButton(f"{EMOJIS['users']} USUÁRIOS", callback_data="admin_users"),
            InlineKeyboardButton(f"{EMOJIS['money']} PAGAMENTOS", callback_data="admin_payments")
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['diamond']} AFILIADOS", callback_data="admin_affiliates"),
            InlineKeyboardButton(f"{EMOJIS['fire']} SAQUES", callback_data="admin_withdrawals")
        ],
        [
            InlineKeyboardButton(f"{EMOJIS['warning']} NOTIFICAÇÕES", callback_data="admin_notifications"),
            InlineKeyboardButton(f"{EMOJIS['book']} RELATÓRIOS", callback_data="admin_reports")
        ],
        [InlineKeyboardButton(f"{EMOJIS['cross']} VOLTAR AO MENU", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado para cancelar operação
    
    Returns:
        Teclado de cancelamento
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['cross']} CANCELAR", callback_data="main_menu")]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard(confirm_callback: str, cancel_callback: str = "cancel") -> InlineKeyboardMarkup:
    """
    Retorna teclado de confirmação genérico
    
    Args:
        confirm_callback: Callback para confirmação
        cancel_callback: Callback para cancelamento
    
    Returns:
        Teclado de confirmação
    """
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['check']} CONFIRMAR", callback_data=confirm_callback),
            InlineKeyboardButton(f"{EMOJIS['cross']} CANCELAR", callback_data=cancel_callback)
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_back_button_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado com apenas botão de voltar
    
    Args:
        callback_data: Callback do botão voltar
    
    Returns:
        Teclado com botão voltar
    """
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['cross']} VOLTAR", callback_data=callback_data)]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def create_dynamic_keyboard(buttons: List[List[Dict]]) -> InlineKeyboardMarkup:
    """
    Cria teclado dinâmico baseado em lista de botões
    
    Args:
        buttons: Lista de listas com dados dos botões
    
    Returns:
        Teclado dinâmico
    """
    keyboard = []
    
    for row in buttons:
        keyboard_row = []
        for button_data in row:
            if "url" in button_data:
                button = InlineKeyboardButton(
                    text=button_data["text"],
                    url=button_data["url"]
                )
            else:
                button = InlineKeyboardButton(
                    text=button_data["text"],
                    callback_data=button_data["callback_data"]
                )
            keyboard_row.append(button)
        keyboard.append(keyboard_row)
    
    return InlineKeyboardMarkup(keyboard)