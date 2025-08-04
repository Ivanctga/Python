"""
Teclados inline para o Imperium™ Bot
Define todos os botões e menus utilizados na interface
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Optional
from config.settings import PLANS, format_currency, EMOJIS

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu principal
    
    Returns:
        Teclado inline do menu principal
    """
    builder = InlineKeyboardBuilder()
    
    # Primeira linha - Comprar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cart']} QUERO ADQUIRIR O IMPERIUM™",
            callback_data="buy_plans"
        )
    )
    
    # Segunda linha - Afiliados
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['users']} SISTEMA DE AFILIADOS",
            callback_data="affiliate_menu"
        )
    )
    
    # Terceira linha - Suporte e canal
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

def get_plans_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado com planos disponíveis
    
    Returns:
        Teclado inline com planos
    """
    builder = InlineKeyboardBuilder()
    
    # Adicionar cada plano
    for plan_key, plan_data in PLANS.items():
        button_text = f"{plan_data['emoji']} {plan_data['name']} - {format_currency(plan_data['price'])}"
        builder.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"select_plan:{plan_key}"
            )
        )
    
    # Botão voltar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR AO MENU",
            callback_data="back_to_main"
        )
    )
    
    return builder.as_markup()

def get_plan_confirmation_keyboard(plan_key: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado de confirmação do plano
    
    Args:
        plan_key: Chave do plano selecionado
    
    Returns:
        Teclado de confirmação
    """
    builder = InlineKeyboardBuilder()
    
    # Confirmar compra
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} CONFIRMAR COMPRA",
            callback_data=f"confirm_plan:{plan_key}"
        )
    )
    
    # Voltar aos planos
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR AOS PLANOS",
            callback_data="buy_plans"
        )
    )
    
    return builder.as_markup()

def get_payment_keyboard(payment_id: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado para pagamento
    
    Args:
        payment_id: ID do pagamento
    
    Returns:
        Teclado de pagamento
    """
    builder = InlineKeyboardBuilder()
    
    # Verificar pagamento
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} VERIFICAR PAGAMENTO",
            callback_data=f"check_payment:{payment_id}"
        )
    )
    
    # Cancelar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} CANCELAR",
            callback_data="cancel_payment"
        )
    )
    
    return builder.as_markup()

def get_affiliate_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu de afiliados
    
    Returns:
        Teclado do menu de afiliados
    """
    builder = InlineKeyboardBuilder()
    
    # Dashboard
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['target']} MEU DASHBOARD",
            callback_data="affiliate_dashboard"
        )
    )
    
    # Link de afiliado
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['rocket']} MEU LINK DE AFILIADO",
            callback_data="my_affiliate_link"
        )
    )
    
    # Solicitar saque
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['money']} SOLICITAR SAQUE",
            callback_data="request_withdrawal"
        )
    )
    
    # Histórico de vendas
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['book']} HISTÓRICO DE VENDAS",
            callback_data="sales_history"
        )
    )
    
    # Voltar ao menu
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR AO MENU",
            callback_data="back_to_main"
        )
    )
    
    return builder.as_markup()

def get_affiliate_dashboard_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do dashboard de afiliados
    
    Returns:
        Teclado do dashboard
    """
    builder = InlineKeyboardBuilder()
    
    # Atualizar dados
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['gear']} ATUALIZAR DADOS",
            callback_data="refresh_affiliate_data"
        )
    )
    
    # Voltar ao menu de afiliados
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data="affiliate_menu"
        )
    )
    
    return builder.as_markup()

def get_withdrawal_confirmation_keyboard(amount: float) -> InlineKeyboardMarkup:
    """
    Retorna teclado de confirmação de saque
    
    Args:
        amount: Valor do saque
    
    Returns:
        Teclado de confirmação
    """
    builder = InlineKeyboardBuilder()
    
    # Confirmar saque
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} CONFIRMAR SAQUE",
            callback_data=f"confirm_withdrawal:{amount}"
        )
    )
    
    # Cancelar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} CANCELAR",
            callback_data="affiliate_menu"
        )
    )
    
    return builder.as_markup()

def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do menu administrativo
    
    Returns:
        Teclado administrativo
    """
    builder = InlineKeyboardBuilder()
    
    # Dashboard
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['target']} DASHBOARD",
            callback_data="admin_dashboard"
        )
    )
    
    # Gerenciamento
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['users']} USUÁRIOS",
            callback_data="admin_users"
        ),
        InlineKeyboardButton(
            text=f"{EMOJIS['money']} PAGAMENTOS",
            callback_data="admin_payments"
        )
    )
    
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['diamond']} AFILIADOS",
            callback_data="admin_affiliates"
        ),
        InlineKeyboardButton(
            text=f"{EMOJIS['fire']} SAQUES",
            callback_data="admin_withdrawals"
        )
    )
    
    # Notificações e relatórios
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['warning']} NOTIFICAÇÕES",
            callback_data="admin_notifications"
        ),
        InlineKeyboardButton(
            text=f"{EMOJIS['book']} RELATÓRIOS",
            callback_data="admin_reports"
        )
    )
    
    # Voltar ao menu
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR AO MENU",
            callback_data="back_to_main"
        )
    )
    
    return builder.as_markup()

def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado do dashboard administrativo
    
    Returns:
        Teclado do dashboard admin
    """
    builder = InlineKeyboardBuilder()
    
    # Atualizar estatísticas
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['gear']} ATUALIZAR DADOS",
            callback_data="refresh_admin_stats"
        )
    )
    
    # Exportar dados
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['book']} EXPORTAR CSV",
            callback_data="export_data_menu"
        )
    )
    
    # Voltar ao menu admin
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data="admin_menu"
        )
    )
    
    return builder.as_markup()

def get_admin_withdrawals_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado para gerenciamento de saques
    
    Returns:
        Teclado de saques
    """
    builder = InlineKeyboardBuilder()
    
    # Ver saques pendentes
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['clock']} SAQUES PENDENTES",
            callback_data="pending_withdrawals"
        )
    )
    
    # Histórico de saques
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['book']} HISTÓRICO DE SAQUES",
            callback_data="withdrawals_history"
        )
    )
    
    # Voltar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data="admin_menu"
        )
    )
    
    return builder.as_markup()

def get_withdrawal_action_keyboard(withdrawal_id: int) -> InlineKeyboardMarkup:
    """
    Retorna teclado para ações em saque específico
    
    Args:
        withdrawal_id: ID da solicitação de saque
    
    Returns:
        Teclado de ações
    """
    builder = InlineKeyboardBuilder()
    
    # Aprovar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} APROVAR",
            callback_data=f"approve_withdrawal:{withdrawal_id}"
        )
    )
    
    # Rejeitar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} REJEITAR",
            callback_data=f"reject_withdrawal:{withdrawal_id}"
        )
    )
    
    # Voltar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['warning']} VOLTAR",
            callback_data="pending_withdrawals"
        )
    )
    
    return builder.as_markup()

def get_export_data_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado para exportação de dados
    
    Returns:
        Teclado de exportação
    """
    builder = InlineKeyboardBuilder()
    
    # Tipos de exportação
    export_options = [
        ("users", "👥 USUÁRIOS"),
        ("payments", "💰 PAGAMENTOS"),
        ("subscriptions", "💎 ASSINATURAS"),
        ("affiliates", "🔗 AFILIADOS"),
        ("withdrawals", "💸 SAQUES")
    ]
    
    for callback, text in export_options:
        builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=f"export:{callback}"
            )
        )
    
    # Voltar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data="admin_dashboard"
        )
    )
    
    return builder.as_markup()

def get_pagination_keyboard(current_page: int, total_pages: int, 
                          callback_prefix: str, extra_buttons: List[Dict] = None) -> InlineKeyboardMarkup:
    """
    Retorna teclado de paginação
    
    Args:
        current_page: Página atual
        total_pages: Total de páginas
        callback_prefix: Prefixo para callbacks
        extra_buttons: Botões extras (opcional)
    
    Returns:
        Teclado de paginação
    """
    builder = InlineKeyboardBuilder()
    
    # Botões de navegação
    nav_buttons = []
    
    if current_page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Anterior",
                callback_data=f"{callback_prefix}:page:{current_page - 1}"
            )
        )
    
    nav_buttons.append(
        InlineKeyboardButton(
            text=f"📄 {current_page}/{total_pages}",
            callback_data="current_page"
        )
    )
    
    if current_page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Próxima ➡️",
                callback_data=f"{callback_prefix}:page:{current_page + 1}"
            )
        )
    
    # Adicionar botões de navegação
    if len(nav_buttons) == 1:
        builder.row(nav_buttons[0])
    elif len(nav_buttons) == 2:
        builder.row(*nav_buttons)
    else:
        builder.row(nav_buttons[0], nav_buttons[1], nav_buttons[2])
    
    # Adicionar botões extras se fornecidos
    if extra_buttons:
        for button_data in extra_buttons:
            builder.row(
                InlineKeyboardButton(
                    text=button_data["text"],
                    callback_data=button_data["callback_data"]
                )
            )
    
    return builder.as_markup()

def get_confirmation_keyboard(confirm_callback: str, cancel_callback: str = "cancel") -> InlineKeyboardMarkup:
    """
    Retorna teclado de confirmação genérico
    
    Args:
        confirm_callback: Callback para confirmação
        cancel_callback: Callback para cancelamento
    
    Returns:
        Teclado de confirmação
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} CONFIRMAR",
            callback_data=confirm_callback
        ),
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} CANCELAR",
            callback_data=cancel_callback
        )
    )
    
    return builder.as_markup()

def get_back_button_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado com apenas botão de voltar
    
    Args:
        callback_data: Callback do botão voltar
    
    Returns:
        Teclado com botão voltar
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data=callback_data
        )
    )
    
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado para cancelar operação
    
    Returns:
        Teclado de cancelamento
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} CANCELAR",
            callback_data="back_to_main"
        )
    )
    
    return builder.as_markup()

def get_url_button_keyboard(text: str, url: str) -> InlineKeyboardMarkup:
    """
    Retorna teclado com botão de URL
    
    Args:
        text: Texto do botão
        url: URL do botão
    
    Returns:
        Teclado com botão URL
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=text,
            url=url
        )
    )
    
    return builder.as_markup()

def get_success_keyboard(next_action: str = "back_to_main") -> InlineKeyboardMarkup:
    """
    Retorna teclado para tela de sucesso
    
    Args:
        next_action: Próxima ação
    
    Returns:
        Teclado de sucesso
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['check']} CONTINUAR",
            callback_data=next_action
        )
    )
    
    return builder.as_markup()

def create_dynamic_keyboard(buttons: List[List[Dict]], row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Cria teclado dinâmico baseado em lista de botões
    
    Args:
        buttons: Lista de listas com dados dos botões
        row_width: Largura da linha (botões por linha)
    
    Returns:
        Teclado dinâmico
    """
    builder = InlineKeyboardBuilder()
    
    for row in buttons:
        row_buttons = []
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
            row_buttons.append(button)
        
        builder.row(*row_buttons)
    
    return builder.as_markup()

def get_notification_keyboard() -> InlineKeyboardMarkup:
    """
    Retorna teclado para notificações administrativas
    
    Returns:
        Teclado de notificações
    """
    builder = InlineKeyboardBuilder()
    
    # Enviar aviso geral
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['warning']} ENVIAR AVISO GERAL",
            callback_data="send_general_notice"
        )
    )
    
    # Notificar afiliados
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['users']} NOTIFICAR AFILIADOS",
            callback_data="notify_affiliates"
        )
    )
    
    # Voltar
    builder.row(
        InlineKeyboardButton(
            text=f"{EMOJIS['cross']} VOLTAR",
            callback_data="admin_menu"
        )
    )
    
    return builder.as_markup()