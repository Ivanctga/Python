"""
Estados do usuário para o Imperium™ Bot
Define todos os estados possíveis dos usuários durante a interação
(Versão simplificada sem dependência do aiogram)
"""

from enum import Enum, auto

class UserStates(Enum):
    """Estados principais do usuário"""
    
    # Estado inicial
    MAIN_MENU = "main_menu"
    
    # Estados de compra
    SELECTING_PLAN = "selecting_plan"
    ENTERING_PHONE = "entering_phone"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_CONFIRMED = "payment_confirmed"
    
    # Estados de afiliados
    AFFILIATE_MENU = "affiliate_menu"
    ENTERING_PIX_KEY = "entering_pix_key"
    WITHDRAWAL_PENDING = "withdrawal_pending"
    
    # Estados administrativos
    ADMIN_MENU = "admin_menu"
    ADMIN_VIEWING_USERS = "admin_viewing_users"
    ADMIN_VIEWING_PAYMENTS = "admin_viewing_payments"
    ADMIN_VIEWING_AFFILIATES = "admin_viewing_affiliates"
    ADMIN_VIEWING_WITHDRAWALS = "admin_viewing_withdrawals"
    ADMIN_SENDING_NOTIFICATION = "admin_sending_notification"
    ADMIN_PROCESSING_WITHDRAWAL = "admin_processing_withdrawal"

class PaymentStates(Enum):
    """Estados específicos do processo de pagamento"""
    
    # Seleção e validação
    PLAN_SELECTED = "plan_selected"
    PHONE_VALIDATION = "phone_validation"
    
    # Processamento do pagamento
    GENERATING_PIX = "generating_pix"
    WAITING_PAYMENT = "waiting_payment"
    CHECKING_PAYMENT = "checking_payment"
    
    # Finalização
    PAYMENT_APPROVED = "payment_approved"
    PAYMENT_REJECTED = "payment_rejected"
    PAYMENT_EXPIRED = "payment_expired"

class AffiliateStates(Enum):
    """Estados específicos do sistema de afiliados"""
    
    # Menu de afiliados
    AFFILIATE_DASHBOARD = "affiliate_dashboard"
    VIEWING_AFFILIATE_STATS = "viewing_affiliate_stats"
    
    # Processo de saque
    REQUESTING_WITHDRAWAL = "requesting_withdrawal"
    PIX_KEY_VALIDATION = "pix_key_validation"
    WITHDRAWAL_CONFIRMATION = "withdrawal_confirmation"
    
    # Gerenciamento
    VIEWING_SALES_HISTORY = "viewing_sales_history"
    MANAGING_REFERRALS = "managing_referrals"

class AdminStates(Enum):
    """Estados específicos do painel administrativo"""
    
    # Dashboard principal
    ADMIN_DASHBOARD = "admin_dashboard"
    VIEWING_STATISTICS = "viewing_statistics"
    
    # Gerenciamento de usuários
    USER_MANAGEMENT = "user_management"
    USER_DETAILS = "user_details"
    USER_EDITING = "user_editing"
    
    # Gerenciamento de pagamentos
    PAYMENT_MANAGEMENT = "payment_management"
    PAYMENT_DETAILS = "payment_details"
    PAYMENT_REFUND = "payment_refund"
    
    # Gerenciamento de afiliados
    AFFILIATE_MANAGEMENT = "affiliate_management"
    AFFILIATE_DETAILS = "affiliate_details"
    
    # Gerenciamento de saques
    WITHDRAWAL_MANAGEMENT = "withdrawal_management"
    WITHDRAWAL_PROCESSING = "withdrawal_processing"
    WITHDRAWAL_REJECTION = "withdrawal_rejection"
    
    # Notificações e alertas
    NOTIFICATION_CENTER = "notification_center"
    SENDING_BROADCAST = "sending_broadcast"
    CREATING_ANNOUNCEMENT = "creating_announcement"
    
    # Relatórios e exportações
    REPORTS_MENU = "reports_menu"
    EXPORTING_DATA = "exporting_data"
    SCHEDULING_REPORTS = "scheduling_reports"
    
    # Configurações do sistema
    SYSTEM_SETTINGS = "system_settings"
    UPDATING_PLANS = "updating_plans"
    MANAGING_ADMINS = "managing_admins"

# Mapeamento de estados para descrições legíveis
STATE_DESCRIPTIONS = {
    # Estados principais
    UserStates.MAIN_MENU: "Menu Principal",
    UserStates.SELECTING_PLAN: "Selecionando Plano",
    UserStates.ENTERING_PHONE: "Inserindo Telefone",
    UserStates.PAYMENT_PENDING: "Pagamento Pendente",
    UserStates.PAYMENT_CONFIRMED: "Pagamento Confirmado",
    UserStates.AFFILIATE_MENU: "Menu de Afiliados",
    UserStates.ENTERING_PIX_KEY: "Inserindo Chave Pix",
    UserStates.WITHDRAWAL_PENDING: "Saque Pendente",
    UserStates.ADMIN_MENU: "Menu Administrativo",
    
    # Estados de pagamento
    PaymentStates.PLAN_SELECTED: "Plano Selecionado",
    PaymentStates.PHONE_VALIDATION: "Validando Telefone",
    PaymentStates.GENERATING_PIX: "Gerando Pix",
    PaymentStates.WAITING_PAYMENT: "Aguardando Pagamento",
    PaymentStates.CHECKING_PAYMENT: "Verificando Pagamento",
    PaymentStates.PAYMENT_APPROVED: "Pagamento Aprovado",
    PaymentStates.PAYMENT_REJECTED: "Pagamento Rejeitado",
    PaymentStates.PAYMENT_EXPIRED: "Pagamento Expirado",
    
    # Estados de afiliados
    AffiliateStates.AFFILIATE_DASHBOARD: "Dashboard de Afiliado",
    AffiliateStates.VIEWING_AFFILIATE_STATS: "Visualizando Estatísticas",
    AffiliateStates.REQUESTING_WITHDRAWAL: "Solicitando Saque",
    AffiliateStates.PIX_KEY_VALIDATION: "Validando Chave Pix",
    AffiliateStates.WITHDRAWAL_CONFIRMATION: "Confirmando Saque",
    AffiliateStates.VIEWING_SALES_HISTORY: "Histórico de Vendas",
    AffiliateStates.MANAGING_REFERRALS: "Gerenciando Indicações",
    
    # Estados administrativos
    AdminStates.ADMIN_DASHBOARD: "Dashboard Admin",
    AdminStates.VIEWING_STATISTICS: "Visualizando Estatísticas",
    AdminStates.USER_MANAGEMENT: "Gerenciamento de Usuários",
    AdminStates.USER_DETAILS: "Detalhes do Usuário",
    AdminStates.PAYMENT_MANAGEMENT: "Gerenciamento de Pagamentos",
    AdminStates.AFFILIATE_MANAGEMENT: "Gerenciamento de Afiliados",
    AdminStates.WITHDRAWAL_MANAGEMENT: "Gerenciamento de Saques",
    AdminStates.NOTIFICATION_CENTER: "Central de Notificações",
    AdminStates.REPORTS_MENU: "Menu de Relatórios",
    AdminStates.SYSTEM_SETTINGS: "Configurações do Sistema",
}

def get_state_description(state) -> str:
    """
    Retorna descrição legível do estado
    
    Args:
        state: Estado do sistema
    
    Returns:
        Descrição do estado
    """
    return STATE_DESCRIPTIONS.get(state, "Estado Desconhecido")

# Estados que permitem cancelamento
CANCELLABLE_STATES = {
    UserStates.SELECTING_PLAN,
    UserStates.ENTERING_PHONE,
    UserStates.ENTERING_PIX_KEY,
    PaymentStates.PHONE_VALIDATION,
    PaymentStates.GENERATING_PIX,
    AffiliateStates.REQUESTING_WITHDRAWAL,
    AffiliateStates.PIX_KEY_VALIDATION,
}

# Estados que requerem dados sensíveis
SENSITIVE_STATES = {
    UserStates.ENTERING_PHONE,
    UserStates.ENTERING_PIX_KEY,
    PaymentStates.PHONE_VALIDATION,
    AffiliateStates.PIX_KEY_VALIDATION,
}

# Estados temporários que expiram (em minutos)
TEMPORARY_STATES = {
    UserStates.PAYMENT_PENDING: 1440,  # 24 horas
    PaymentStates.WAITING_PAYMENT: 1440,
    PaymentStates.CHECKING_PAYMENT: 60,  # 1 hora
    AffiliateStates.WITHDRAWAL_CONFIRMATION: 60,
}

def is_cancellable_state(state) -> bool:
    """
    Verifica se o estado permite cancelamento
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se cancelável, False caso contrário
    """
    return state in CANCELLABLE_STATES

def is_sensitive_state(state) -> bool:
    """
    Verifica se o estado envolve dados sensíveis
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se sensível, False caso contrário
    """
    return state in SENSITIVE_STATES

def get_state_timeout(state) -> int:
    """
    Retorna tempo limite do estado em minutos
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        Tempo limite em minutos ou 0 se não tem limite
    """
    return TEMPORARY_STATES.get(state, 0)