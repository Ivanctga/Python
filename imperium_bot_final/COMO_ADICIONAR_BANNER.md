# 🖼️ Como Adicionar sua Imagem Personalizada no /start

## 📁 Onde colocar a imagem:

Você pode colocar sua imagem em qualquer one desses locais (o bot procura nesta ordem):

### **Opção 1 - Raiz do projeto (MAIS FÁCIL):**
```
imperium_bot_final/
├── banner.jpg          ← COLOQUE AQUI
├── banner.png          ← OU AQUI
├── imperium_banner.jpg
├── imperium_banner.png
├── main.py
└── ...
```

### **Opção 2 - Pasta assets:**
```
imperium_bot_final/
├── assets/
│   ├── banner.jpg      ← OU AQUI
│   ├── banner.png      
│   ├── imperium_banner.jpg
│   └── imperium_banner.png
├── main.py
└── ...
```

### **Opção 3 - Pasta images:**
```
imperium_bot_final/
├── images/
│   ├── banner.jpg      ← OU AQUI
│   └── banner.png      
├── main.py
└── ...
```

## 📝 Formatos aceitos:
- ✅ **JPG** (.jpg, .jpeg)
- ✅ **PNG** (.png)

## 📏 Recomendações de tamanho:
- **Largura:** 1200px (máximo)
- **Altura:** 600-800px 
- **Peso:** Máximo 5MB
- **Qualidade:** Boa resolução mas não muito pesada

## 🚀 Como funciona:

1. **COM imagem:** 
   ```
   [SUA IMAGEM PERSONALIZADA]
   🚨 ᎥᗰᑭᗴᖇᎥᑌᗰ™, João, você ainda está fora do jogo?
   💻 Enquanto você espera, milhares de profissionais...
   [BOTÕES DO MENU]
   ```

2. **SEM imagem (fallback):**
   ```
   🚨 ᎥᗰᑭᗴᖇᎥᑌᗰ™, João, você ainda está fora do jogo?
   💻 Enquanto você espera, milhares de profissionais...
   [BOTÕES DO MENU]
   ```

## 💡 Dicas:

- **Nome mais fácil:** Use `banner.jpg` na raiz do projeto
- **Teste sempre** enviando /start depois de adicionar
- **Verifique os logs** para ver se a imagem foi encontrada
- **Crie uma imagem impactante** que represente o Imperium™

## 🔧 Troubleshooting:

**Imagem não aparece?**
1. Verifique se o nome está correto
2. Verifique se está em uma das pastas listadas
3. Olhe os logs do bot para ver erros
4. Teste com uma imagem menor

**Bot lento para carregar?**
- Reduza o tamanho da imagem
- Comprima a qualidade (70-80%)

---

✅ **Pronto!** Sua imagem personalizada vai aparecer sempre que alguém digitar `/start`!