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
        "description": "📅 Acesso completo por 30 dias\n🚀 Teste todas as IAs premium\n💰 Ideal para começar a lucrar",
        "emoji": "💰"
    },
    "TRIMESTRAL": {
        "name": "TRIMESTRAL", 
        "price": 79.90,
        "duration_days": 90,
        "description": "📅 Acesso completo por 90 dias\n💎 Economize 33% + bônus exclusivos\n🔥 Mais popular entre profissionais",
        "emoji": "💎"
    },
    "SEMESTRAL": {
        "name": "SEMESTRAL",
        "price": 149.90,
        "duration_days": 180,
        "description": "📅 Acesso completo por 180 dias\n🔥 Economize 50% + vantagens VIP\n⚡ Máximo retorno do investimento",
        "emoji": "🔥"
    },
    "ANUAL": {
        "name": "ANUAL",
        "price": 249.90,
        "duration_days": 365,
        "description": "📅 Acesso completo por 365 dias\n⭐ Melhor custo-benefício absoluto\n👑 Status VIP premium + benefícios exclusivos",
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
🚨 <b>ᎥᗰᑭᗴᖇᎥᑌᗰ™, {name}, você ainda está fora do jogo?</b>

💻 <b>Enquanto você espera, milhares de profissionais já estão lucrando pesado com as melhores IAs e automações do mercado — com apenas alguns cliques.</b>

🔹 <b>Por que o ᎥᗰᑭᗴᖇᎥᑌᗰ™ é indispensável?</b>
✅ Mais de <b>R$ 20.000</b> em ferramentas premium liberadas de imediato.
✅ Operação segura com Dicloak e proxies SOCKS5 — performance máxima, anonimato real e risco zero.
✅ Atualizações mensais e novas soluções direto no seu painel.
✅ Suporte ágil e reposição garantida — suas IAs nunca ficam fora do ar.

🎁 <b>BÔNUS EXCLUSIVOS ᎥᗰᑭᗴᖇᎥᑌᗰ™:</b>
🔄 Ferramentas novas toda semana, sem custo adicional.
🎟 Sorteios de contas Paramount+, HBO Max, Disney+ e outras plataformas premium.
🛠 Biblioteca com 200+ ferramentas extras organizadas para você escalar.
📞 Suporte 24h por dia, 7 dias por semana — sempre que você precisar.

⚠️ <b>Cada minuto de indecisão é um passo atrás dos seus concorrentes.</b>
Essa oportunidade pode sair do ar a qualquer momento, mas seus resultados podem começar hoje.

🔗 <b>Entre agora no ᎥᗰᑭᗴᖇᎥᑌᗰ™ e transforme IA em lucro.</b>

🤝 <b>Sistema de Afiliados Disponível</b>
Ganhe 20% de comissão em cada venda que você indicar!

📲 Escolha uma opção abaixo para começar:
"""

BUY_MESSAGE = """
🛒 <b>ADQUIRIR O ᎥᗰᑭᗴᖇᎥᑌᗰ™</b>

💎 <b>Escolha o plano ideal para começar a lucrar hoje:</b>

🔥 <b>O que você ganha sendo membro:</b>
• ✅ Mais de <b>R$ 20.000</b> em ferramentas premium
• ✅ Operação segura com Dicloak e proxies SOCKS5
• ✅ Atualizações semanais sem custo adicional
• ✅ Suporte 24h/7dias por semana
• ✅ Grupo VIP exclusivo com estratégias

🤖 <b>Arsenal completo de IAs premium:</b>
• 🧠 Claude (Anthropic)
• 💻 Cursor AI
• 🌟 ChatGPT Plus
• 🚀 Grok 4
• 🔍 Perplexity Pro
• ⚫ Blackbox AI
• 🎬 Netflix, Prime Video, Disney+, HBO Max
• 🛠 200+ ferramentas extras organizadas

🎁 <b>BÔNUS EXCLUSIVOS:</b>
• 🔄 Ferramentas novas toda semana
• 🎟 Sorteios de plataformas premium
• 📊 Performance máxima garantida
• 🔒 Anonimato real e risco zero

⚠️ <b>Não perca mais tempo enquanto outros lucram!</b>

👇 Selecione seu plano e comece agora:
"""

AFFILIATE_MESSAGE = """
👥 <b>SISTEMA DE AFILIADOS ᎥᗰᑭᗴᖇᎥᑌᗰ™</b>

💰 <b>Ganhe 20% de comissão em cada venda e transforme sua rede em uma máquina de lucro!</b>

🎯 <b>Como funciona o sistema que já enriqueceu centenas:</b>
1️⃣ Você gera seu link único de afiliado
2️⃣ Compartilha com seus contatos (família, amigos, redes sociais)
3️⃣ Recebe 20% de comissão de cada venda automaticamente
4️⃣ Saca via Pix quando quiser, sem burocracia

💎 <b>Por que nosso programa de afiliados é diferente:</b>
• ✅ Comissão de <b>20%</b> (uma das maiores do mercado)
• ✅ Saque mínimo de apenas <b>R$ 10,00</b>
• ✅ Pagamento via Pix instantâneo e automático
• ✅ Dashboard em tempo real para acompanhar vendas
• ✅ Suporte dedicado 24h para afiliados
• ✅ Material de divulgação pronto para usar

📊 <b>Potencial de ganhos reais:</b>
• Plano Mensal (R$ 29,90) = <b>R$ 5,98</b> por venda
• Plano Trimestral (R$ 79,90) = <b>R$ 15,98</b> por venda
• Plano Semestral (R$ 149,90) = <b>R$ 29,98</b> por venda
• Plano Anual (R$ 249,90) = <b>R$ 49,98</b> por venda

🚀 <b>Meta conservadora: 5 vendas/mês = R$ 149,90 extras!</b>
💪 <b>Afiliados top fazem R$ 2.000+ por mês!</b>

🤖 <b>Você está vendendo o futuro: acesso às melhores IAs do mundo!</b>

⚠️ <b>Quanto mais você espera, mais dinheiro está perdendo.</b>

👇 Escolha uma opção e comece a lucrar:
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
🎉 <b>PAGAMENTO APROVADO! BEM-VINDO AO ᎥᗰᑭᗴᖇᎥᑌᗰ™!</b>

✅ <b>Parabéns! Sua assinatura foi ativada e você acabou de entrar no seleto grupo de profissionais que lucram com IA!</b>

🚀 <b>Seus próximos passos para o sucesso:</b>
1️⃣ Entre no grupo VIP exclusivo abaixo
2️⃣ Acesse sua plataforma ᎥᗰᑭᗴᖇᎥᑌᗰ™ premium
3️⃣ Comece a usar suas R$ 20.000+ em ferramentas
4️⃣ Explore todas as IAs e automações disponíveis

📱 <b>Acesso ao Grupo VIP Exclusivo:</b>
{vip_group_link}

💎 <b>Detalhes da sua assinatura premium:</b>
• 📅 Válida até: {end_date}
• 🤖 Acesso total a todas as IAs liberado
• 🛠 200+ ferramentas extras à sua disposição
• 🔒 Operação segura com Dicloak e proxies SOCKS5
• 🔄 Renovação automática disponível

🎁 <b>Seus bônus exclusivos já estão ativos:</b>
• 🔄 Ferramentas novas toda semana
• 🎟 Participação automática nos sorteios
• 📞 Suporte 24h/7dias prioritário

⚡ <b>Agora é hora de transformar IA em lucro real!</b>

🆘 <b>Suporte premium 24h:</b> {support_contact}

🔥 <b>Você fez a escolha certa! Bem-vindo ao futuro!</b> 🚀
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