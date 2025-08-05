@echo off
chcp 65001 > nul
cls

:: Script de inicialização do Imperium™ Bot para Windows
:: Compatível com Windows 10/11 e Windows RDP

echo.
echo ██╗███╗   ███╗██████╗ ███████╗██████╗ ██╗██╗   ██╗███╗   ███╗
echo ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗██║██║   ██║████╗ ████║
echo ██║██╔████╔██║██████╔╝█████╗  ██████╔╝██║██║   ██║██╔████╔██║
echo ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║   ██║██║╚██╔╝██║
echo ██║██║ ╚═╝ ██║██║     ███████╗██║  ██║██║╚██████╔╝██║ ╚═╝ ██║
echo ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
echo.
echo === INICIANDO IMPERIUM™ BOT ===
echo.

:: Verificar se Python está instalado
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo Instalando Python...
    
    :: Baixar e instalar Python se não estiver instalado
    if not exist "python-installer.exe" (
        echo Baixando Python...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile 'python-installer.exe'"
    )
    
    echo Executando instalador do Python...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Aguardar instalação
    timeout /t 30 /nobreak >nul
    
    :: Verificar novamente
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Falha na instalação do Python
        pause
        exit /b 1
    )
)
echo ✅ Python encontrado

:: Verificar pip
echo Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado!
    echo Instalando pip...
    python -m ensurepip --upgrade
)
echo ✅ pip encontrado

:: Criar ambiente virtual se não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual encontrado
)

:: Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo ✅ Ambiente virtual ativado

:: Verificar arquivo .env
if not exist ".env" (
    echo ❌ Arquivo .env não encontrado!
    echo Criando arquivo .env modelo...
    
    (
        echo # --- TELEGRAM ---
        echo BOT_TOKEN=SEU_TOKEN_DO_BOT_TELEGRAM
        echo.
        echo # --- MERCADO PAGO ^(PRODUÇÃO^) ---
        echo MP_PUBLIC_KEY=SUA_CHAVE_PUBLICA_MERCADO_PAGO
        echo MP_ACCESS_TOKEN=SEU_ACCESS_TOKEN_MERCADO_PAGO
        echo.
        echo # --- CANAIS E TÓPICOS ---
        echo CANAL_LOGS_ID=ID_DO_SEU_CANAL_DE_LOGS_PRIVADO
        echo TOPICO_GERAL_AVISOS=LINK_DO_SEU_TOPICO_DE_AVISOS_PUBLICO
    ) > .env
    
    echo 📝 Configure o arquivo .env antes de continuar!
    pause
    exit /b 1
)

:: Verificar se .env está configurado
findstr "SEU_TOKEN_DO_BOT_TELEGRAM" .env >nul
if %errorlevel% equ 0 (
    echo ❌ Configure o BOT_TOKEN no arquivo .env
    pause
    exit /b 1
)

findstr "SEU_ACCESS_TOKEN_MERCADO_PAGO" .env >nul
if %errorlevel% equ 0 (
    echo ❌ Configure o MP_ACCESS_TOKEN no arquivo .env
    pause
    exit /b 1
)

echo ✅ Arquivo .env configurado

:: Instalar/atualizar dependências
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Dependências instaladas

:: Criar diretórios necessários
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports
echo ✅ Diretórios verificados

:: Verificar dependências Python
echo Verificando dependências...
python -c "import telegram, aiosqlite, mercadopago, qrcode; print('✅ Dependências verificadas')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro nas dependências
    echo Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ✅ Todas as verificações passaram!
echo.
echo 🚀 Iniciando Imperium™ Bot...
echo Pressione Ctrl+C para parar o bot
echo.

:: Iniciar bot
python main.py

:: Se chegou aqui, o bot foi interrompido
echo.
echo 🛑 Bot finalizado
pause