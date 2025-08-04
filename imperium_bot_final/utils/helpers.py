"""
Funções auxiliares para validações e formatações do Imperium™ Bot
Inclui validações de telefone, Pix, formatações e utilitários gerais
"""

import re
import phonenumbers
import validators
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta
import uuid
import hashlib
from utils.logger import logger

def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Valida e formata número de telefone brasileiro
    
    Args:
        phone: Número de telefone
    
    Returns:
        Tupla (is_valid, formatted_phone)
    """
    try:
        # Remove caracteres não numéricos
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        # Verificar se tem 10 ou 11 dígitos
        if len(clean_phone) not in [10, 11]:
            return False, "Telefone deve ter 10 ou 11 dígitos"
        
        # Verificar se não começa com 0
        if clean_phone.startswith('0'):
            return False, "Telefone não pode começar com 0"
        
        # Para telefones com 11 dígitos, o terceiro dígito deve ser 9
        if len(clean_phone) == 11 and clean_phone[2] != '9':
            return False, "Celulares devem ter 9 como terceiro dígito"
        
        # Verificar DDDs válidos (principais cidades brasileiras)
        valid_area_codes = [
            '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
            '21', '22', '24',  # RJ
            '27', '28',  # ES
            '31', '32', '33', '34', '35', '37', '38',  # MG
            '41', '42', '43', '44', '45', '46',  # PR
            '47', '48', '49',  # SC
            '51', '53', '54', '55',  # RS
            '61',  # DF
            '62', '64',  # GO
            '63',  # TO
            '65', '66',  # MT
            '67',  # MS
            '68',  # AC
            '69',  # RO
            '71', '73', '74', '75', '77',  # BA
            '79',  # SE
            '81', '87',  # PE
            '82',  # AL
            '83',  # PB
            '84',  # RN
            '85', '88',  # CE
            '86', '89',  # PI
            '91', '93', '94',  # PA
            '92', '97',  # AM
            '95',  # RR
            '96',  # AP
            '98', '99'   # MA
        ]
        
        area_code = clean_phone[:2]
        if area_code not in valid_area_codes:
            return False, f"DDD {area_code} não é válido"
        
        # Verificar com phonenumbers para validação adicional
        try:
            parsed = phonenumbers.parse(f"+55{clean_phone}", None)
            if not phonenumbers.is_valid_number(parsed):
                return False, "Número de telefone inválido"
        except:
            pass  # Continuar mesmo se a validação externa falhar
        
        return True, clean_phone
        
    except Exception as e:
        logger.error(f"Erro na validação de telefone: {e}")
        return False, "Erro na validação"

def validate_pix_key(pix_key: str) -> Tuple[bool, str, str]:
    """
    Valida chave Pix e identifica o tipo
    
    Args:
        pix_key: Chave Pix a ser validada
    
    Returns:
        Tupla (is_valid, pix_type, formatted_key)
    """
    try:
        pix_key = pix_key.strip()
        
        # CPF (11 dígitos)
        if re.match(r'^\d{11}$', pix_key):
            if validate_cpf(pix_key):
                formatted = format_cpf(pix_key)
                return True, "CPF", formatted
            else:
                return False, "", "CPF inválido"
        
        # CNPJ (14 dígitos)
        if re.match(r'^\d{14}$', pix_key):
            if validate_cnpj(pix_key):
                formatted = format_cnpj(pix_key)
                return True, "CNPJ", formatted
            else:
                return False, "", "CNPJ inválido"
        
        # E-mail
        if validators.email(pix_key):
            return True, "EMAIL", pix_key.lower()
        
        # Telefone
        phone_valid, formatted_phone = validate_phone(pix_key)
        if phone_valid:
            return True, "TELEFONE", f"+55{formatted_phone}"
        
        # Chave aleatória (UUID format)
        if re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', pix_key.lower()):
            return True, "CHAVE_ALEATORIA", pix_key.lower()
        
        return False, "", "Formato de chave Pix não reconhecido"
        
    except Exception as e:
        logger.error(f"Erro na validação de chave Pix: {e}")
        return False, "", "Erro na validação"

def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro
    
    Args:
        cpf: CPF a ser validado
    
    Returns:
        True se válido, False caso contrário
    """
    try:
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^\d]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não são todos iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcula segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        # Verifica se os dígitos estão corretos
        return cpf[-2:] == f"{digit1}{digit2}"
        
    except Exception:
        return False

def validate_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ brasileiro
    
    Args:
        cnpj: CNPJ a ser validado
    
    Returns:
        True se válido, False caso contrário
    """
    try:
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^\d]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verifica se não são todos iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcula primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Calcula segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        # Verifica se os dígitos estão corretos
        return cnpj[-2:] == f"{digit1}{digit2}"
        
    except Exception:
        return False

def format_cpf(cpf: str) -> str:
    """Formata CPF para exibição"""
    cpf = re.sub(r'[^\d]', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ para exibição"""
    cnpj = re.sub(r'[^\d]', '', cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def format_phone(phone: str) -> str:
    """Formata telefone para exibição"""
    phone = re.sub(r'[^\d]', '', phone)
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone

def format_currency(value: float) -> str:
    """
    Formata valor monetário para exibição brasileira
    
    Args:
        value: Valor a ser formatado
    
    Returns:
        String formatada (ex: "R$ 29,90")
    """
    return f"R$ {value:.2f}".replace(".", ",")

def parse_currency(currency_str: str) -> float:
    """
    Converte string de moeda para float
    
    Args:
        currency_str: String de moeda (ex: "R$ 29,90")
    
    Returns:
        Valor float
    """
    try:
        # Remove símbolos e espaços
        clean_str = re.sub(r'[R$\s]', '', currency_str)
        # Substitui vírgula por ponto
        clean_str = clean_str.replace(',', '.')
        return float(clean_str)
    except:
        return 0.0

def format_date_br(date_obj: datetime) -> str:
    """
    Formata data para padrão brasileiro
    
    Args:
        date_obj: Objeto datetime
    
    Returns:
        String formatada (ex: "25/12/2023 às 15:30")
    """
    return date_obj.strftime("%d/%m/%Y às %H:%M")

def format_date_br_short(date_obj: datetime) -> str:
    """
    Formata data para padrão brasileiro curto
    
    Args:
        date_obj: Objeto datetime
    
    Returns:
        String formatada (ex: "25/12/2023")
    """
    return date_obj.strftime("%d/%m/%Y")

def calculate_time_remaining(expiration_date: datetime) -> str:
    """
    Calcula tempo restante até expiração
    
    Args:
        expiration_date: Data de expiração
    
    Returns:
        String com tempo restante
    """
    try:
        now = datetime.now()
        if now >= expiration_date:
            return "Expirado"
        
        remaining = expiration_date - now
        
        if remaining.days > 0:
            return f"{remaining.days}d {remaining.seconds // 3600}h"
        elif remaining.seconds >= 3600:
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            return f"{hours}h {minutes}min"
        else:
            minutes = remaining.seconds // 60
            return f"{minutes}min"
    except:
        return "Erro ao calcular"

def generate_unique_id() -> str:
    """
    Gera ID único para transações
    
    Returns:
        String com ID único
    """
    return str(uuid.uuid4())

def generate_referral_code(user_id: int) -> str:
    """
    Gera código de referência único para afiliado
    
    Args:
        user_id: ID do usuário
    
    Returns:
        Código de referência
    """
    # Combina user_id com timestamp para garantir unicidade
    data = f"{user_id}_{int(datetime.now().timestamp())}"
    hash_object = hashlib.md5(data.encode())
    return hash_object.hexdigest()[:8].upper()

def create_affiliate_link(bot_username: str, user_id: int) -> str:
    """
    Cria link de afiliado
    
    Args:
        bot_username: Username do bot
        user_id: ID do afiliado
    
    Returns:
        Link de afiliado
    """
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def extract_referrer_from_start(start_param: str) -> Optional[int]:
    """
    Extrai ID do referenciador do parâmetro /start
    
    Args:
        start_param: Parâmetro do comando /start
    
    Returns:
        ID do referenciador ou None
    """
    try:
        if start_param and start_param.startswith("ref_"):
            return int(start_param[4:])
        return None
    except:
        return None

def validate_email(email: str) -> bool:
    """
    Valida endereço de e-mail
    
    Args:
        email: E-mail a ser validado
    
    Returns:
        True se válido, False caso contrário
    """
    return validators.email(email) is True

def sanitize_text(text: str, max_length: int = 100) -> str:
    """
    Sanitiza texto removendo caracteres especiais
    
    Args:
        text: Texto a ser sanitizado
        max_length: Comprimento máximo
    
    Returns:
        Texto sanitizado
    """
    # Remove caracteres HTML/Markdown perigosos
    text = re.sub(r'[<>]', '', text)
    # Limita o comprimento
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text.strip()

def format_percentage(value: float) -> str:
    """
    Formata porcentagem para exibição
    
    Args:
        value: Valor decimal (0.20 = 20%)
    
    Returns:
        String formatada (ex: "20%")
    """
    return f"{value * 100:.0f}%"

def calculate_commission(amount: float, rate: float) -> float:
    """
    Calcula comissão com base no valor e taxa
    
    Args:
        amount: Valor base
        rate: Taxa de comissão (0.20 = 20%)
    
    Returns:
        Valor da comissão
    """
    return round(amount * rate, 2)

def is_valid_telegram_id(user_id: int) -> bool:
    """
    Verifica se é um ID válido do Telegram
    
    Args:
        user_id: ID a ser verificado
    
    Returns:
        True se válido, False caso contrário
    """
    return isinstance(user_id, int) and user_id > 0 and user_id < 10**10

def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
    """
    Mascara dados sensíveis para logs
    
    Args:
        data: Dados a serem mascarados
        mask_char: Caractere para mascarar
    
    Returns:
        String mascarada
    """
    if len(data) <= 4:
        return mask_char * len(data)
    
    # Mostra apenas os 2 primeiros e 2 últimos caracteres
    return data[:2] + mask_char * (len(data) - 4) + data[-2:]

def get_user_display_name(user_data: Dict) -> str:
    """
    Obtém nome de exibição do usuário
    
    Args:
        user_data: Dados do usuário
    
    Returns:
        Nome formatado para exibição
    """
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    username = user_data.get('username', '')
    
    if first_name:
        name = first_name
        if last_name:
            name += f" {last_name}"
        return name
    elif username:
        return f"@{username}"
    else:
        return f"Usuário {user_data.get('user_id', 'Unknown')}"

def create_pagination_text(current_page: int, total_pages: int, 
                          items_per_page: int, total_items: int) -> str:
    """
    Cria texto de paginação
    
    Args:
        current_page: Página atual
        total_pages: Total de páginas
        items_per_page: Items por página
        total_items: Total de items
    
    Returns:
        Texto de paginação formatado
    """
    start_item = (current_page - 1) * items_per_page + 1
    end_item = min(current_page * items_per_page, total_items)
    
    return f"📄 Página {current_page}/{total_pages} • Items {start_item}-{end_item} de {total_items}"

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca texto se exceder o limite
    
    Args:
        text: Texto a ser truncado
        max_length: Comprimento máximo
        suffix: Sufixo a ser adicionado
    
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def is_business_hours() -> bool:
    """
    Verifica se está em horário comercial (8h às 18h)
    
    Returns:
        True se em horário comercial, False caso contrário
    """
    now = datetime.now()
    return 8 <= now.hour < 18

def get_greeting() -> str:
    """
    Retorna saudação baseada no horário
    
    Returns:
        Saudação apropriada
    """
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"