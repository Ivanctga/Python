"""
Configurações centrais do Imperium™ Bot
Contém todas as configurações necessárias para operação do sistema
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# ===== CONFIGURAÇÕES DO TELEGRAM =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_LOGS_ID = os.getenv("CANAL_LOGS_ID")
TOPICO_GERAL_AVISOS = os.getenv("TOPICO_GERAL_AVISOS")

# ===== CONFIGURAÇÕES DO MERCADO PAGO =====
MP_PUBLIC_KEY = os.getenv("MP_PUBLIC_KEY")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# ===== IDS DOS ADMINISTRADORES =====
# Adicione aqui os IDs dos usuários que terão acesso ao painel administrativo
ADMIN_IDS = [
    123456789,  # Substitua pelo seu ID real
    987654321,  # Adicione mais IDs conforme necessário
]

# ===== PLANOS DISPONÍVEIS =====
PLANS = {
    "MENSAL": {
        "name": "MENSAL",
        "price": 29.90,
        "duration_days": 30,
        "description": "📅 Acesso por 30 dias ao pacote completo",
        "emoji": "💰"
    },
    "TRIMESTRAL": {
        "name": "TRIMESTRAL", 
        "price": 79.90,
        "duration_days": 90,
        "description": "📅 Acesso por 90 dias ao pacote completo\n💎 Economize 33%!",
        "emoji": "💎"
    },
    "SEMESTRAL": {
        "name": "SEMESTRAL",
        "price": 149.90,
        "duration_days": 180,
        "description": "📅 Acesso por 180 dias ao pacote completo\n🔥 Economize 50%!",
        "emoji": "🔥"
    },
    "ANUAL": {
        "name": "ANUAL",
        "price": 249.90,
        "duration_days": 365,
        "description": "📅 Acesso por 365 dias ao pacote completo\n⭐ Melhor custo-benefício!",
        "emoji": "⭐"
    }
}

# ===== CONFIGURAÇÕES DO SISTEMA DE AFILIADOS =====
COMMISSION_RATE = 0.20  # 20% de comissão
MIN_WITHDRAWAL_AMOUNT = 10.00  # Valor mínimo para saque R$ 10,00

# ===== LINKS E CONTATOS =====
VIP_GROUP_LINK = "https://t.me/seu_grupo_vip"  # Link do grupo VIP
SUPPORT_CONTACT = "@seu_suporte"  # Contato de suporte
CHANNEL_LINK = "https://t.me/seu_canal"  # Link do canal principal

# ===== MENSAGENS PADRÃO =====
WELCOME_MESSAGE = """
🎯 <b>Bem-vindo ao IMPERIUM™, {name}!</b>

🤖 <b>O que você encontrará aqui:</b>
• 🧠 Claude (Anthropic)
• 💻 Cursor AI
• 🌟 ChatGPT Plus
• 🚀 Grok 4
• 🔍 Perplexity Pro
• ⚫ Blackbox AI
• 🎬 Streamings Premium
• 🎯 E muito mais!

💎 <b>Plataforma Imperial de IAs</b>
Um universo completo de inteligências artificiais premium ao seu alcance!

🤝 <b>Sistema de Afiliados Disponível</b>
Ganhe 20% de comissão em cada venda que você indicar!

📲 Escolha uma opção abaixo para começar:
"""

BUY_MESSAGE = """
🛒 <b>ADQUIRIR O IMPERIUM™</b>

💎 Escolha o plano ideal para você:

🔥 <b>Vantagens de ser membro:</b>
• ✅ Acesso ilimitado a todas as IAs
• ✅ Atualizações constantes
• ✅ Suporte premium
• ✅ Grupo VIP exclusivo
• ✅ Plataforma completa de ferramentas

🤖 <b>Todos os planos incluem:</b>
• 🧠 Claude (Anthropic)
• 💻 Cursor AI
• 🌟 ChatGPT Plus
• 🚀 Grok 4
• 🔍 Perplexity Pro
• ⚫ Blackbox AI
• 🎬 Netflix, Prime Video, Disney+
• 📊 Streamings e ferramentas premium

👇 Selecione seu plano:
"""

AFFILIATE_MESSAGE = """
👥 <b>SISTEMA DE AFILIADOS IMPERIUM™</b>

💰 <b>Ganhe 20% de comissão em cada venda!</b>

🎯 <b>Como funciona:</b>
1️⃣ Você gera seu link único
2️⃣ Compartilha com seus contatos
3️⃣ Recebe 20% de cada venda
4️⃣ Saca via Pix quando quiser

💎 <b>Vantagens:</b>
• ✅ Comissão de 20% (uma das maiores do mercado)
• ✅ Saque mínimo de apenas R$ 10,00
• ✅ Pagamento via Pix instantâneo
• ✅ Dashboard para acompanhar vendas
• ✅ Suporte dedicado para afiliados

📊 <b>Exemplo de ganhos:</b>
• Plano Mensal (R$ 29,90) = R$ 5,98 por venda
• Plano Trimestral (R$ 79,90) = R$ 15,98 por venda
• Plano Semestral (R$ 149,90) = R$ 29,98 por venda
• Plano Anual (R$ 249,90) = R$ 49,98 por venda

🚀 <b>Meta de 5 vendas/mês = R$ 149,90 extras!</b>
🤖 <b>Ajude pessoas a acessar IAs premium!</b>

👇 Escolha uma opção:
"""

PAYMENT_INSTRUCTIONS = """
💳 <b>INSTRUÇÕES DE PAGAMENTO</b>

📱 <b>Como pagar via Pix:</b>

1️⃣ <b>Pelo QR Code:</b>
   • Abra seu app bancário
   • Escaneie o código QR acima
   • Confirme o pagamento

2️⃣ <b>Por Copia e Cola:</b>
   • Copie o código abaixo
   • Cole no seu app bancário
   • Confirme o pagamento

⏰ <b>Importante:</b>
• Pagamento expira em 24 horas
• Após pagar, clique em "✅ VERIFICAR PAGAMENTO"
• Acesso liberado automaticamente
• Em caso de dúvidas: {support_contact}

🔒 <b>Pagamento 100% seguro via Mercado Pago</b>
"""

SUCCESS_MESSAGE = """
🎉 <b>PAGAMENTO APROVADO!</b>

✅ <b>Sua assinatura foi ativada com sucesso!</b>

🎯 <b>Próximos passos:</b>
1️⃣ Entre no grupo VIP abaixo
2️⃣ Acesse a plataforma Imperium™
3️⃣ Comece a usar todas as IAs premium

📱 <b>Acesso ao Grupo VIP:</b>
{vip_group_link}

💎 <b>Sua assinatura:</b>
• 📅 Válida até: {end_date}
• 🤖 Acesso a todas as IAs liberado
• 🔄 Renovação automática disponível

🆘 <b>Precisa de ajuda?</b>
Entre em contato: {support_contact}

Bem-vindo ao IMPERIUM™! 🚀
"""

PAYMENT_PENDING_MESSAGE = """
⏳ <b>PAGAMENTO PENDENTE</b>

🔍 Status atual: Aguardando confirmação

💡 <b>O que fazer:</b>
• Se já pagou, aguarde alguns minutos
• Clique novamente em "✅ VERIFICAR PAGAMENTO"
• O sistema verifica automaticamente

⏰ <b>Tempo restante:</b> {time_remaining}

❗ <b>Ainda não pagou?</b>
Use o QR Code ou código Pix acima para efetuar o pagamento.

🆘 <b>Problemas?</b> Contate: {support_contact}
"""

PAYMENT_EXPIRED_MESSAGE = """
⌛ <b>PAGAMENTO EXPIRADO</b>

❌ O tempo para pagamento deste Pix expirou.

🔄 <b>Para continuar:</b>
• Clique em "🛒 QUERO ADQUIRIR O IMPERIUM™"
• Selecione novamente seu plano
• Um novo Pix será gerado

💡 <b>Dica:</b> O Pix tem validade de 24 horas para maior segurança.

🆘 <b>Precisa de ajuda?</b> Contate: {support_contact}
"""

# ===== CONFIGURAÇÕES DE LOGS =====
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/imperium_bot.log"

# ===== CONFIGURAÇÕES DE AGENDAMENTO =====
DAILY_REPORT_TIME = "09:00"  # Horário do relatório diário
SUBSCRIPTION_CHECK_INTERVAL = 6  # Verificação de assinaturas a cada 6 horas
DATABASE_BACKUP_TIME = "03:00"  # Backup do banco às 3h da manhã

# ===== MENSAGENS DE ERRO =====
ERROR_MESSAGES = {
    "invalid_phone": "❌ Telefone inválido! Digite apenas números com DDD (10 ou 11 dígitos).\n\nExemplo: 11999887766",
    "invalid_pix_key": "❌ Chave Pix inválida! Verifique o formato e tente novamente.",
    "insufficient_balance": "❌ Saldo insuficiente para saque. Valor mínimo: R$ {min_amount:.2f}",
    "user_not_found": "❌ Usuário não encontrado no sistema.",
    "payment_error": "❌ Erro ao processar pagamento. Tente novamente ou contate o suporte.",
    "already_subscribed": "✅ Você já possui uma assinatura ativa até {end_date}!",
    "access_denied": "❌ Acesso negado. Apenas administradores podem usar este comando.",
    "maintenance": "🔧 Sistema em manutenção. Tente novamente em alguns minutos."
}

# ===== VALIDAÇÃO DE CONFIGURAÇÕES =====
def validate_config():
    """Valida se todas as configurações essenciais estão presentes"""
    required_vars = [
        ("BOT_TOKEN", BOT_TOKEN),
        ("MP_ACCESS_TOKEN", MP_ACCESS_TOKEN),
        ("MP_PUBLIC_KEY", MP_PUBLIC_KEY),
        ("CANAL_LOGS_ID", CANAL_LOGS_ID)
    ]
    
    missing_vars = []
    for var_name, var_value in required_vars:
        if not var_value or var_value.startswith("SEU_"):
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente obrigatórias não configuradas: {', '.join(missing_vars)}")
    
    return True

# ===== FORMATAÇÃO DE VALORES =====
def format_currency(value: float) -> str:
    """Formata valor monetário para exibição"""
    return f"R$ {value:.2f}".replace(".", ",")

def format_date(date_obj) -> str:
    """Formata data para exibição brasileira"""
    return date_obj.strftime("%d/%m/%Y às %H:%M")

# ===== CONFIGURAÇÕES DE EMOJI =====
EMOJIS = {
    "money": "💰",
    "diamond": "💎", 
    "fire": "🔥",
    "star": "⭐",
    "cart": "🛒",
    "users": "👥",
    "admin": "⚙️",
    "check": "✅",
    "cross": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "crown": "👑",
    "rocket": "🚀",
    "target": "🎯",
    "phone": "📱",
    "calendar": "📅",
    "clock": "⏰",
    "gear": "🔧",
    "book": "📚",
    "game": "🎮"
}