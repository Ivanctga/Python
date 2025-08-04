#!/bin/bash

# Script de instalação do Imperium™ Bot
# Compatível com Linux, Termux e macOS

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "████████╗███╗   ███╗██████╗ ███████╗██████╗ ██╗██╗   ██╗███╗   ███╗"
echo "╚══██╔══╝████╗ ████║██╔══██╗██╔════╝██╔══██╗██║██║   ██║████╗ ████║"
echo "   ██║   ██╔████╔██║██████╔╝█████╗  ██████╔╝██║██║   ██║██╔████╔██║"
echo "   ██║   ██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║   ██║██║╚██╔╝██║"
echo "   ██║   ██║ ╚═╝ ██║██║     ███████╗██║  ██║██║╚██████╔╝██║ ╚═╝ ██║"
echo "   ╚═╝   ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝"
echo -e "${NC}"
echo -e "${GREEN}=== INSTALADOR AUTOMÁTICO DO IMPERIUM™ BOT ===${NC}"
echo ""

# Detectar sistema operacional
detect_os() {
    if [ -f /data/data/com.termux/files/usr/bin/pkg ]; then
        OS="termux"
        echo -e "${BLUE}Sistema detectado: Termux (Android)${NC}"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        echo -e "${BLUE}Sistema detectado: Linux${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        echo -e "${BLUE}Sistema detectado: macOS${NC}"
    else
        echo -e "${RED}Sistema operacional não suportado!${NC}"
        exit 1
    fi
}

# Verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Instalar Python
install_python() {
    echo -e "${YELLOW}Verificando Python...${NC}"
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
        echo -e "${GREEN}Python $PYTHON_VERSION encontrado${NC}"
        
        # Verificar se versão é >= 3.8
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            echo -e "${GREEN}✅ Versão do Python é compatível${NC}"
        else
            echo -e "${RED}❌ Python 3.8+ é necessário${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Instalando Python...${NC}"
        case $OS in
            "termux")
                pkg update && pkg install python
                ;;
            "linux")
                if command_exists apt; then
                    sudo apt update && sudo apt install -y python3 python3-pip
                elif command_exists yum; then
                    sudo yum install -y python3 python3-pip
                elif command_exists dnf; then
                    sudo dnf install -y python3 python3-pip
                else
                    echo -e "${RED}Gerenciador de pacotes não suportado${NC}"
                    exit 1
                fi
                ;;
            "macos")
                if command_exists brew; then
                    brew install python
                else
                    echo -e "${RED}Homebrew não encontrado. Instale em: https://brew.sh${NC}"
                    exit 1
                fi
                ;;
        esac
    fi
}

# Instalar pip
install_pip() {
    echo -e "${YELLOW}Verificando pip...${NC}"
    
    if command_exists pip3; then
        echo -e "${GREEN}✅ pip3 encontrado${NC}"
    else
        echo -e "${YELLOW}Instalando pip...${NC}"
        case $OS in
            "termux")
                pkg install python-pip
                ;;
            "linux")
                if command_exists apt; then
                    sudo apt install -y python3-pip
                elif command_exists yum; then
                    sudo yum install -y python3-pip
                elif command_exists dnf; then
                    sudo dnf install -y python3-pip
                fi
                ;;
            "macos")
                python3 -m ensurepip --upgrade
                ;;
        esac
    fi
}

# Instalar dependências do sistema
install_system_deps() {
    echo -e "${YELLOW}Instalando dependências do sistema...${NC}"
    
    case $OS in
        "termux")
            pkg install -y libjpeg-turbo libpng zlib freetype
            ;;
        "linux")
            if command_exists apt; then
                sudo apt install -y libjpeg-dev libpng-dev zlib1g-dev libfreetype6-dev
            elif command_exists yum; then
                sudo yum install -y libjpeg-turbo-devel libpng-devel zlib-devel freetype-devel
            elif command_exists dnf; then
                sudo dnf install -y libjpeg-turbo-devel libpng-devel zlib-devel freetype-devel
            fi
            ;;
        "macos")
            if command_exists brew; then
                brew install jpeg libpng freetype
            fi
            ;;
    esac
}

# Criar ambiente virtual
create_venv() {
    echo -e "${YELLOW}Criando ambiente virtual...${NC}"
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
    else
        echo -e "${GREEN}✅ Ambiente virtual já existe${NC}"
    fi
}

# Ativar ambiente virtual
activate_venv() {
    echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
}

# Instalar dependências Python
install_python_deps() {
    echo -e "${YELLOW}Instalando dependências Python...${NC}"
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Dependências Python instaladas${NC}"
}

# Criar diretórios necessários
create_dirs() {
    echo -e "${YELLOW}Criando diretórios...${NC}"
    
    mkdir -p logs
    mkdir -p exports
    
    echo -e "${GREEN}✅ Diretórios criados${NC}"
}

# Verificar arquivo .env
check_env_file() {
    echo -e "${YELLOW}Verificando arquivo .env...${NC}"
    
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ Arquivo .env não encontrado!${NC}"
        echo -e "${YELLOW}Criando arquivo .env modelo...${NC}"
        
        cat > .env << EOF
# --- TELEGRAM ---
BOT_TOKEN=SEU_TOKEN_DO_BOT_TELEGRAM

# --- MERCADO PAGO (PRODUÇÃO) ---
MP_PUBLIC_KEY=SUA_CHAVE_PUBLICA_MERCADO_PAGO
MP_ACCESS_TOKEN=SEU_ACCESS_TOKEN_MERCADO_PAGO

# --- CANAIS E TÓPICOS ---
CANAL_LOGS_ID=ID_DO_SEU_CANAL_DE_LOGS_PRIVADO
TOPICO_GERAL_AVISOS=LINK_DO_SEU_TOPICO_DE_AVISOS_PUBLICO
EOF
        
        echo -e "${YELLOW}📝 Configure o arquivo .env antes de iniciar o bot!${NC}"
    else
        echo -e "${GREEN}✅ Arquivo .env encontrado${NC}"
    fi
}

# Teste de importação
test_imports() {
    echo -e "${YELLOW}Testando importações...${NC}"
    
    python3 -c "
import sys
try:
    import aiogram
    import aiosqlite
    import mercadopago
    import qrcode
    import PIL
    print('✅ Todas as dependências foram importadas com sucesso!')
except ImportError as e:
    print(f'❌ Erro ao importar: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Teste de importação passou${NC}"
    else
        echo -e "${RED}❌ Erro no teste de importação${NC}"
        exit 1
    fi
}

# Função principal
main() {
    echo -e "${BLUE}Iniciando instalação...${NC}"
    echo ""
    
    detect_os
    install_python
    install_pip
    install_system_deps
    create_venv
    activate_venv
    install_python_deps
    create_dirs
    check_env_file
    test_imports
    
    echo ""
    echo -e "${GREEN}🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉${NC}"
    echo ""
    echo -e "${BLUE}Próximos passos:${NC}"
    echo -e "${YELLOW}1.${NC} Configure o arquivo .env com seus tokens"
    echo -e "${YELLOW}2.${NC} Execute: ${GREEN}./start_bot.sh${NC}"
    echo ""
    echo -e "${BLUE}Para iniciar o bot manualmente:${NC}"
    echo -e "${GREEN}source venv/bin/activate && python main.py${NC}"
    echo ""
}

# Executar função principal
main