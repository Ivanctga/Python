# 🤖 IMPERIUM™ BOT v2.0 - GUIA DE INSTALAÇÃO

## 📦 O que você baixou:

✅ **Bot 100% migrado** de aiogram para python-telegram-bot  
✅ **Links únicos VIP** (não compartilháveis)  
✅ **QR Code + Copia e Cola** nos pagamentos  
✅ **Banner personalizado** no /start  
✅ **Todas as funcionalidades** originais mantidas  

---

## 🚀 INSTALAÇÃO RÁPIDA:

### **1. Requisitos:**
- **Python 3.11 ou 3.12** (3.13 tem incompatibilidade temporária)
- **Sistema Linux/Windows/Mac**

### **2. Instalar dependências:**
```bash
cd imperium_bot_final
pip install -r requirements.txt
```

### **3. Configurar variáveis (.env):**
Crie o arquivo `.env` na raiz:
```bash
# TELEGRAM
BOT_TOKEN=SEU_TOKEN_DO_BOTFATHER
CANAL_LOGS_ID=-1001234567890
TOPICO_GERAL_AVISOS=1

# MERCADO PAGO
MP_PUBLIC_KEY=SUA_CHAVE_PUBLICA
MP_ACCESS_TOKEN=SEU_ACCESS_TOKEN
```

### **4. Adicionar sua imagem (OPCIONAL):**
- Coloque sua imagem como `banner.jpg` na pasta raiz
- Ou veja o arquivo `COMO_ADICIONAR_BANNER.md`

### **5. Rodar o bot:**
```bash
python3 main.py
```

---

## ⚙️ CONFIGURAÇÃO DETALHADA:

### **📝 Arquivo .env completo:**
```bash
# ===== TELEGRAM =====
BOT_TOKEN=123456789:ABCDEFGH-SEU-TOKEN-AQUI
CANAL_LOGS_ID=-1001234567890
TOPICO_GERAL_AVISOS=1

# ===== MERCADO PAGO =====
MP_PUBLIC_KEY=APP_USR-12345678-1234-1234-1234-123456789012
MP_ACCESS_TOKEN=APP_USR-1234567890123456-012345-abcdef123456789012345678901234567890-1234567890
```

### **🔧 Configurações importantes:**

**1. IDs de Administradores** (`config/settings.py`):
```python
ADMIN_IDS = [
    123456789,  # Seu ID do Telegram
    987654321,  # Outros admins
]
```

**2. Link do Grupo VIP** (`config/settings.py`):
```python
VIP_GROUP_LINK = "https://t.me/seu_grupo_vip"
SUPPORT_CONTACT = "@seu_suporte"
```

**3. Planos e Preços** (`config/settings.py`):
```python
PLANS = {
    "MENSAL": {
        "name": "MENSAL",
        "price": 79.90,  # ← Ajuste o preço aqui
        "duration_days": 30,
        ...
    }
}
```

---

## 🎯 FUNCIONALIDADES IMPLEMENTADAS:

### ✅ **1. Links únicos VIP:**
- Cada usuário recebe link exclusivo
- `member_limit=1` (não compartilhável)
- Expira após primeiro uso

### ✅ **2. QR Code + Copia e Cola:**
```
💳 PAGAMENTO PIX GERADO
[QR CODE IMAGE]
📋 Código Pix (Copia e Cola):
00020126580014br.gov.bcb.pix...
```

### ✅ **3. Banner personalizado /start:**
```
[SUA IMAGEM PERSONALIZADA]
🚨 IMPERIUM™ texto de boas-vindas...
[BOTÕES DO MENU]
```

### ✅ **4. Biblioteca atualizada:**
- ❌ `aiogram` (removido)
- ✅ `python-telegram-bot 20.8`
- ✅ Compatível com Python 3.11/3.12

---

## 🛠️ COMANDOS ÚTEIS:

### **Iniciar bot:**
```bash
python3 main.py
```

### **Rodar em background:**
```bash
nohup python3 main.py > bot.log 2>&1 &
```

### **Ver logs:**
```bash
tail -f logs/imperium_bot.log
```

### **Parar bot:**
```bash
pkill -f main.py
```

---

## 🔧 TROUBLESHOOTING:

### **Erro "ModuleNotFoundError":**
```bash
pip install -r requirements.txt --upgrade
```

### **Python 3.13 não funciona:**
- Use Python 3.12 ou 3.11
- Aguarde atualização da biblioteca

### **Token inválido:**
- Verifique o `.env`
- Crie novo bot no @BotFather

### **Pagamentos não funcionam:**
- Configure Mercado Pago no `.env`
- Teste com valores pequenos primeiro

### **Banner não aparece:**
- Verifique se `banner.jpg` existe
- Veja arquivo `COMO_ADICIONAR_BANNER.md`

---

## 📞 SUPORTE:

**Bot funcionando?** ✅ Todas as funcionalidades implementadas!

**Dúvidas de configuração?** Consulte os arquivos:
- `config/settings.py` - Configurações gerais
- `COMO_ADICIONAR_BANNER.md` - Banner personalizado
- `logs/imperium_bot.log` - Logs do sistema

---

## 📋 CHECKLIST FINAL:

- [ ] Python 3.11/3.12 instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` configurado
- [ ] Bot token válido
- [ ] Mercado Pago configurado
- [ ] IDs de admin atualizados
- [ ] Banner personalizado adicionado (opcional)
- [ ] Bot rodando (`python3 main.py`)

**🎉 Pronto! Seu bot Imperium™ v2.0 está funcionando!**