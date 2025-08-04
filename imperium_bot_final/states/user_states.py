"""
Estados do FSM (Finite State Machine) para o Imperium™ Bot
Define todos os estados possíveis dos usuários durante a interação
"""

from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """Estados principais do usuário"""
    
    # Estado inicial
    MAIN_MENU = State()
    
    # Estados de compra
    SELECTING_PLAN = State()
    ENTERING_PHONE = State()
    PAYMENT_PENDING = State()
    PAYMENT_CONFIRMED = State()
    
    # Estados de afiliados
    AFFILIATE_MENU = State()
    ENTERING_PIX_KEY = State()
    WITHDRAWAL_PENDING = State()
    
    # Estados administrativos
    ADMIN_MENU = State()
    ADMIN_VIEWING_USERS = State()
    ADMIN_VIEWING_PAYMENTS = State()
    ADMIN_VIEWING_AFFILIATES = State()
    ADMIN_VIEWING_WITHDRAWALS = State()
    ADMIN_SENDING_NOTIFICATION = State()
    ADMIN_PROCESSING_WITHDRAWAL = State()

class PaymentStates(StatesGroup):
    """Estados específicos do processo de pagamento"""
    
    # Seleção e validação
    PLAN_SELECTED = State()
    PHONE_VALIDATION = State()
    
    # Processamento do pagamento
    GENERATING_PIX = State()
    WAITING_PAYMENT = State()
    CHECKING_PAYMENT = State()
    
    # Finalização
    PAYMENT_APPROVED = State()
    PAYMENT_REJECTED = State()
    PAYMENT_EXPIRED = State()

class AffiliateStates(StatesGroup):
    """Estados específicos do sistema de afiliados"""
    
    # Menu de afiliados
    AFFILIATE_DASHBOARD = State()
    VIEWING_AFFILIATE_STATS = State()
    
    # Processo de saque
    REQUESTING_WITHDRAWAL = State()
    PIX_KEY_VALIDATION = State()
    WITHDRAWAL_CONFIRMATION = State()
    
    # Gerenciamento
    VIEWING_SALES_HISTORY = State()
    MANAGING_REFERRALS = State()

class AdminStates(StatesGroup):
    """Estados específicos do painel administrativo"""
    
    # Dashboard principal
    ADMIN_DASHBOARD = State()
    VIEWING_STATISTICS = State()
    
    # Gerenciamento de usuários
    USER_MANAGEMENT = State()
    USER_DETAILS = State()
    USER_EDITING = State()
    
    # Gerenciamento de pagamentos
    PAYMENT_MANAGEMENT = State()
    PAYMENT_DETAILS = State()
    PAYMENT_REFUND = State()
    
    # Gerenciamento de afiliados
    AFFILIATE_MANAGEMENT = State()
    AFFILIATE_DETAILS = State()
    
    # Gerenciamento de saques
    WITHDRAWAL_MANAGEMENT = State()
    WITHDRAWAL_PROCESSING = State()
    WITHDRAWAL_REJECTION = State()
    
    # Notificações e alertas
    NOTIFICATION_CENTER = State()
    SENDING_BROADCAST = State()
    CREATING_ANNOUNCEMENT = State()
    
    # Relatórios e exportações
    REPORTS_MENU = State()
    EXPORTING_DATA = State()
    SCHEDULING_REPORTS = State()
    
    # Configurações do sistema
    SYSTEM_SETTINGS = State()
    UPDATING_PLANS = State()
    MANAGING_ADMINS = State()

class ConversationStates(StatesGroup):
    """Estados para conversações e inputs específicos"""
    
    # Entrada de dados
    WAITING_TEXT_INPUT = State()
    WAITING_NUMBER_INPUT = State()
    WAITING_DATE_INPUT = State()
    WAITING_FILE_UPLOAD = State()
    
    # Confirmações
    WAITING_CONFIRMATION = State()
    PROCESSING_REQUEST = State()
    
    # Feedback e suporte
    PROVIDING_FEEDBACK = State()
    CONTACTING_SUPPORT = State()
    REPORTING_ISSUE = State()

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
    
    # Estados de conversação
    ConversationStates.WAITING_TEXT_INPUT: "Aguardando Texto",
    ConversationStates.WAITING_NUMBER_INPUT: "Aguardando Número",
    ConversationStates.WAITING_CONFIRMATION: "Aguardando Confirmação",
    ConversationStates.PROCESSING_REQUEST: "Processando Solicitação",
    ConversationStates.PROVIDING_FEEDBACK: "Fornecendo Feedback",
    ConversationStates.CONTACTING_SUPPORT: "Contatando Suporte",
}

def get_state_description(state) -> str:
    """
    Retorna descrição legível do estado
    
    Args:
        state: Estado do FSM
    
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
    ConversationStates.WAITING_TEXT_INPUT,
    ConversationStates.WAITING_NUMBER_INPUT,
    ConversationStates.WAITING_CONFIRMATION,
}

# Estados que requerem dados sensíveis
SENSITIVE_STATES = {
    UserStates.ENTERING_PHONE,
    UserStates.ENTERING_PIX_KEY,
    PaymentStates.PHONE_VALIDATION,
    AffiliateStates.PIX_KEY_VALIDATION,
}

# Estados temporários que expiram
TEMPORARY_STATES = {
    UserStates.PAYMENT_PENDING: 1440,  # 24 horas em minutos
    PaymentStates.WAITING_PAYMENT: 1440,
    PaymentStates.CHECKING_PAYMENT: 60,  # 1 hora
    AffiliateStates.WITHDRAWAL_CONFIRMATION: 60,
    ConversationStates.WAITING_CONFIRMATION: 30,  # 30 minutos
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

def is_admin_state(state) -> bool:
    """
    Verifica se é um estado administrativo
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se é estado admin, False caso contrário
    """
    return isinstance(state, AdminStates)

def is_payment_state(state) -> bool:
    """
    Verifica se é um estado de pagamento
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se é estado de pagamento, False caso contrário
    """
    return isinstance(state, PaymentStates)

def is_affiliate_state(state) -> bool:
    """
    Verifica se é um estado de afiliado
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se é estado de afiliado, False caso contrário
    """
    return isinstance(state, AffiliateStates)

# Estados que requerem keyboard específico
KEYBOARD_STATES = {
    UserStates.MAIN_MENU: "main_menu",
    UserStates.SELECTING_PLAN: "plans",
    UserStates.AFFILIATE_MENU: "affiliate",
    UserStates.ADMIN_MENU: "admin",
    PaymentStates.WAITING_PAYMENT: "payment_pending",
    AffiliateStates.AFFILIATE_DASHBOARD: "affiliate_dashboard",
    AdminStates.ADMIN_DASHBOARD: "admin_dashboard",
}

def get_keyboard_for_state(state) -> str:
    """
    Retorna o tipo de keyboard para o estado
    
    Args:
        state: Estado atual
    
    Returns:
        Tipo de keyboard ou None
    """
    return KEYBOARD_STATES.get(state)

# Transições de estado permitidas
ALLOWED_TRANSITIONS = {
    UserStates.MAIN_MENU: [
        UserStates.SELECTING_PLAN,
        UserStates.AFFILIATE_MENU,
        UserStates.ADMIN_MENU,
    ],
    UserStates.SELECTING_PLAN: [
        UserStates.MAIN_MENU,
        UserStates.ENTERING_PHONE,
        PaymentStates.PLAN_SELECTED,
    ],
    UserStates.ENTERING_PHONE: [
        UserStates.MAIN_MENU,
        UserStates.SELECTING_PLAN,
        PaymentStates.PHONE_VALIDATION,
    ],
    PaymentStates.PHONE_VALIDATION: [
        PaymentStates.GENERATING_PIX,
        UserStates.ENTERING_PHONE,
    ],
    PaymentStates.GENERATING_PIX: [
        PaymentStates.WAITING_PAYMENT,
        UserStates.MAIN_MENU,
    ],
    PaymentStates.WAITING_PAYMENT: [
        PaymentStates.CHECKING_PAYMENT,
        PaymentStates.PAYMENT_APPROVED,
        PaymentStates.PAYMENT_EXPIRED,
        UserStates.MAIN_MENU,
    ],
    # Adicionar mais transições conforme necessário
}

def is_valid_transition(from_state, to_state) -> bool:
    """
    Verifica se a transição entre estados é válida
    
    Args:
        from_state: Estado atual
        to_state: Estado destino
    
    Returns:
        True se transição é válida, False caso contrário
    """
    allowed = ALLOWED_TRANSITIONS.get(from_state, [])
    return to_state in allowed or to_state == UserStates.MAIN_MENU  # Sempre permitir voltar ao menu

# Estados que requerem limpeza de dados
CLEANUP_STATES = {
    PaymentStates.PAYMENT_EXPIRED,
    PaymentStates.PAYMENT_REJECTED,
    UserStates.PAYMENT_CONFIRMED,
    AffiliateStates.WITHDRAWAL_CONFIRMATION,
}

def requires_cleanup(state) -> bool:
    """
    Verifica se o estado requer limpeza de dados
    
    Args:
        state: Estado a ser verificado
    
    Returns:
        True se requer limpeza, False caso contrário
    """
    return state in CLEANUP_STATES