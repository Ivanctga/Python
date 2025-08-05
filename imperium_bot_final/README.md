# 🚀 Imperium™ Bot

Um bot completo para Telegram focado em vendas de acesso a plataforma de IAs premium, sistema de afiliados e gestão administrativa robusta.

## 📋 Sobre o Projeto

O **Imperium™ Bot** é uma solução completa para automação de vendas de acesso a plataforma de IAs premium via Telegram, incluindo:

- 🛒 **Sistema de Vendas**: Venda de planos de acesso com pagamento via Pix (Mercado Pago)
- 🤖 **Plataforma de IAs**: Claude, ChatGPT, Cursor, Grok 4, Perplexity, Blackbox AI e mais
- 👥 **Sistema de Afiliados**: Comissões automáticas de 20% para indicações
- ⚙️ **Painel Administrativo**: Dashboard completo com estatísticas e gerenciamento
- 📊 **Relatórios**: Exportação de dados e relatórios automáticos
- 🔄 **Agendamento**: Tarefas automáticas e backups
- 🔒 **Segurança**: Validações robustas e logs detalhados

## 🎯 Funcionalidades Principais

### 💳 Sistema de Pagamentos
- Integração completa com Mercado Pago
- Geração automática de QR Code Pix
- Verificação automática de pagamentos
- Múltiplos planos configuráveis

### 🤝 Sistema de Afiliados
- Links únicos de referência
- Comissão de 20% automática
- Saque via Pix com validação
- Dashboard de vendas para afiliados

### 📊 Painel Administrativo
- Estatísticas em tempo real
- Gerenciamento de usuários e pagamentos
- Aprovação/rejeição de saques
- Exportação de dados em CSV
- Envio de notificações

### 🔧 Recursos Técnicos
- FSM (Finite State Machine) robusto
- Sistema de logs local e remoto
- Agendamento de tarefas automáticas
- Suporte multiplataforma
- Validações completas

## 📱 Compatibilidade

### Sistemas Operacionais Suportados:
- 🐧 **Linux** (Ubuntu, Debian, CentOS, etc.)
- 📱 **Termux** (Android)
- 🍎 **macOS**
- 🪟 **Windows** (10/11 + RDP)

### Requisitos:
- Python 3.8+
- Banco de dados SQLite
- Acesso à internet
- Tokens do Telegram e Mercado Pago

## 🚀 Instalação

### 📋 Pré-requisitos

1. **Token do Bot do Telegram**:
   - Acesse [@BotFather](https://t.me/BotFather)
   - Crie um novo bot com `/newbot`
   - Anote o token fornecido

2. **Credenciais do Mercado Pago**:
   - Acesse [Mercado Pago Developers](https://developers.mercadopago.com)
   - Obtenha `Access Token` e `Public Key`

3. **Canal de Logs** (opcional):
   - Crie um canal privado no Telegram
   - Adicione o bot como administrador
   - Anote o ID do canal

### 🔧 Instalação Automática

#### Linux / macOS / Termux:
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd imperium_bot_final

# 2. Execute o instalador
chmod +x install.sh
./install.sh

# 3. Configure o arquivo .env
nano .env

# 4. Inicie o bot
chmod +x start_bot.sh
./start_bot.sh
```

#### Windows:
```cmd
REM 1. Baixe e extraia o projeto
REM 2. Execute o instalador
start_bot.bat

REM O script irá:
REM - Instalar Python automaticamente se necessário
REM - Criar ambiente virtual
REM - Instalar dependências
REM - Configurar o projeto
```

### ⚙️ Configuração Manual

1. **Instalar Python 3.8+**
2. **Criar ambiente virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar .env**:
   ```env
   BOT_TOKEN=seu_token_do_telegram
   MP_ACCESS_TOKEN=seu_access_token_mercado_pago
   MP_PUBLIC_KEY=sua_public_key_mercado_pago
   CANAL_LOGS_ID=id_do_canal_de_logs
   TOPICO_GERAL_AVISOS=link_do_topico_avisos
   ```

5. **Iniciar o bot**:
   ```bash
   python main.py
   ```

## 🎮 Como Usar

### 👤 Para Usuários

1. **Iniciar**: `/start`
2. **Comprar**: Clique em "🛒 QUERO ADQUIRIR O IMPERIUM™"
3. **Escolher plano**: Selecione o plano desejado
4. **Informar telefone**: Digite seu número para contato
5. **Pagar**: Use o QR Code Pix gerado
6. **Verificar**: Clique em "✅ VERIFICAR PAGAMENTO"
7. **Acessar**: Entre no grupo VIP após confirmação

### 🤝 Para Afiliados

1. **Acessar**: Clique em "👥 SISTEMA DE AFILIADOS"
2. **Gerar link**: Clique em "🔗 MEU LINK DE AFILIADO"
3. **Compartilhar**: Envie seu link único
4. **Acompanhar**: Veja vendas no dashboard
5. **Sacar**: Solicite saque via Pix (mín. R$ 50)

### ⚙️ Para Administradores

1. **Acessar**: `/admin` ou botão no menu
2. **Dashboard**: Veja estatísticas em tempo real
3. **Gerenciar**: Usuários, pagamentos, afiliados
4. **Saques**: Aprovar/rejeitar solicitações
5. **Relatórios**: Exportar dados em CSV
6. **Notificar**: Enviar avisos para usuários

## 📊 Planos Configuráveis

```python
PLANS = {
    "MENSAL": {
        "name": "MENSAL",
        "price": 79.90,
        "duration_days": 30,
        "description": "📅 Acesso completo por 30 dias",
        "emoji": "💰"
    },
    "TRIMESTRAL": {
        "name": "TRIMESTRAL",
        "price": 215.70,
        "duration_days": 90,
        "description": "📅 Acesso completo por 90 dias",
        "emoji": "💎"
    },
    # E mais planos...
}
```

## 🔧 Personalização

### 📝 Mensagens
Edite `config/settings.py` para personalizar:
- Mensagens de boas-vindas
- Textos dos botões
- Mensagens de erro
- Templates de notificação

### 💰 Comissões
```python
COMMISSION_RATE = 0.20  # 20% de comissão
MIN_WITHDRAWAL_AMOUNT = 50.00  # Valor mínimo para saque
```

### 👨‍💼 Administradores
```python
ADMIN_IDS = [
    123456789,  # Seu ID do Telegram
    987654321,  # Outro admin
]
```

## 📁 Estrutura do Projeto

```
imperium_bot_final/
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências Python
├── .env                   # Variáveis de ambiente
├── install.sh             # Instalador Linux/macOS/Termux
├── start_bot.sh           # Iniciador Linux/macOS/Termux
├── start_bot.bat          # Iniciador Windows
├── config/
│   └── settings.py        # Configurações centrais
├── handlers/              # Handlers do bot
│   ├── start_handler.py   # Comando /start e menu
│   └── payment_handler.py # Fluxo de pagamentos
├── payments/              # Sistema de pagamentos
│   ├── mercado_pago.py    # Integração MP
│   └── qr_generator.py    # Geração de QR Code
├── database/
│   └── models.py          # Modelo do banco SQLite
├── utils/
│   ├── helpers.py         # Funções auxiliares
│   └── logger.py          # Sistema de logs
├── keyboards/
│   └── inline_keyboards.py # Teclados inline
├── states/
│   └── user_states.py     # Estados FSM
├── admin_panel/
│   └── scheduler.py       # Agendador de tarefas
├── assets/
│   └── imperium_banner.jpg # Banner do bot
├── logs/                  # Logs do sistema
├── exports/               # Arquivos CSV exportados
└── tests/                 # Testes (opcional)
```

## 🛡️ Segurança

### 🔒 Validações Implementadas
- **Telefone**: Formato brasileiro com DDD
- **Chave Pix**: CPF, CNPJ, e-mail, telefone, chave aleatória
- **Pagamentos**: Verificação automática no Mercado Pago
- **Estados**: FSM robusto contra travamentos
- **Acesso**: Controle de permissões por ID

### 📊 Logs e Monitoramento
- **Logs locais**: Arquivo rotativo com backup
- **Logs remotos**: Envio para canal do Telegram
- **Eventos rastreados**: Vendas, saques, erros, acessos
- **Relatórios**: Automáticos e sob demanda

## 🔄 Tarefas Automáticas

- **📊 Relatório diário**: 09:00 (configurável)
- **💾 Backup do banco**: 03:00 (configurável)
- **🔍 Verificação de assinaturas**: A cada 6 horas
- **🧹 Limpeza de logs**: Remoção de logs antigos

## 🆘 Suporte e Troubleshooting

### ❓ Problemas Comuns

1. **Bot não inicia**:
   - Verifique se o token está correto no `.env`
   - Confirme se todas as dependências estão instaladas
   - Execute `./install.sh` novamente

2. **Pagamentos não funcionam**:
   - Verifique credenciais do Mercado Pago
   - Confirme se está usando credenciais de produção
   - Teste com um pagamento real

3. **QR Code não aparece**:
   - Verifique se as dependências de imagem estão instaladas
   - Em Termux: `pkg install libjpeg-turbo libpng`
   - O bot possui fallback para apenas texto

4. **Logs remotos não chegam**:
   - Verifique se o `CANAL_LOGS_ID` está correto
   - Confirme se o bot é admin do canal
   - Teste enviando uma mensagem manual

### 🔧 Debug Mode

Para debug detalhado, edite `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 📞 Contato

Para suporte adicional:
- 📧 E-mail: suporte@seudominio.com
- 💬 Telegram: @seu_suporte
- 📚 Documentação: [Link da documentação]

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🎉 Agradecimentos

- **Python-telegram-bot**: Framework do bot Telegram
- **Mercado Pago**: API de pagamentos
- **SQLite**: Banco de dados
- **QRCode**: Geração de códigos QR
- **APScheduler**: Agendamento de tarefas

---

<div align="center">

**🚀 Desenvolvido com ❤️ para automatizar vendas no Telegram 🚀**

</div>