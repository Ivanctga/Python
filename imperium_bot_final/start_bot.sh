#!/bin/bash

# Script de inicialização do Imperium™ Bot
# Compatível com Linux, Termux e macOS

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner de inicialização
echo -e "${BLUE}"
echo "██╗███╗   ███╗██████╗ ███████╗██████╗ ██╗██╗   ██╗███╗   ███╗"
echo "██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██║██║   ██║████╗ ████║"
echo "██║██╔████╔██║██████╔╝█████╗  ██████╔╝██║██║   ██║██╔████╔██║"
echo "██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║   ██║██║╚██╔╝██║"
echo "██║██║ ╚═╝ ██║██║     ███████╗██║  ██║██║╚██████╔╝██║ ╚═╝ ██║"
echo "╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝"
echo -e "${NC}"
echo -e "${GREEN}=== INICIANDO IMPERIUM™ BOT ===${NC}"
echo ""

# Verificar se ambiente virtual existe
check_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ Ambiente virtual não encontrado!${NC}"
        echo -e "${YELLOW}Execute primeiro: ./install.sh${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Ambiente virtual encontrado${NC}"
}

# Ativar ambiente virtual
activate_venv() {
    echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
}

# Verificar arquivo .env
check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ Arquivo .env não encontrado!${NC}"
        echo -e "${YELLOW}Crie o arquivo .env com suas configurações${NC}"
        exit 1
    fi
    
    # Verificar se variáveis essenciais estão configuradas
    if grep -q "SEU_TOKEN_DO_BOT_TELEGRAM" .env; then
        echo -e "${RED}❌ Configure o BOT_TOKEN no arquivo .env${NC}"
        exit 1
    fi
    
    if grep -q "SEU_ACCESS_TOKEN_MERCADO_PAGO" .env; then
        echo -e "${RED}❌ Configure o MP_ACCESS_TOKEN no arquivo .env${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Arquivo .env configurado${NC}"
}

# Verificar dependências Python
check_dependencies() {
    echo -e "${YELLOW}Verificando dependências...${NC}"
    
    python3 -c "
import sys
try:
    import aiogram
    import aiosqlite
    import mercadopago
    import qrcode
    import PIL
    print('✅ Dependências verificadas')
except ImportError as e:
    print(f'❌ Dependência ausente: {e}')
    print('Execute: pip install -r requirements.txt')
    sys.exit(1)
" || exit 1
}

# Criar diretórios necessários
ensure_dirs() {
    echo -e "${YELLOW}Verificando diretórios...${NC}"
    mkdir -p logs
    mkdir -p exports
    echo -e "${GREEN}✅ Diretórios verificados${NC}"
}

# Função de limpeza em caso de interrupção
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Bot interrompido pelo usuário${NC}"
    echo -e "${BLUE}👋 Até logo!${NC}"
    exit 0
}

# Capturar sinais de interrupção
trap cleanup SIGINT SIGTERM

# Iniciar bot
start_bot() {
    echo -e "${GREEN}🚀 Iniciando Imperium™ Bot...${NC}"
    echo -e "${BLUE}Pressione Ctrl+C para parar o bot${NC}"
    echo ""
    
    python3 main.py
}

# Função principal
main() {
    echo -e "${BLUE}Verificações iniciais...${NC}"
    
    check_venv
    activate_venv
    check_env
    check_dependencies
    ensure_dirs
    
    echo ""
    echo -e "${GREEN}✅ Todas as verificações passaram!${NC}"
    echo ""
    
    start_bot
}

# Executar função principal
main