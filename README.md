# Organizador Mudae - Guia de Uso

## O que é?
Um programa visual para organizar seus casados do Mudae sem digitar comandos! Funciona como o Mage Note Manager - você pode arrastar e soltar para reorganizar na ordem que quiser.

## Como usar?

### 1️⃣ Pegar os dados do Mudae
- No Discord, use o comando: `$mmsaty+ri-c+x+ko`
- Copie **TODO** o output (pode ser bem longo)
- Cole no arquivo `dados.txt` neste diretório

### 2️⃣ Rodar o programa
**Windows**: Clique duas vezes em `RODAR.bat`

**Alternativa**: 
```bash
python organizador.py
```

### 3️⃣ Reorganizar seus personagens
- A interface mostra todos os seus casados em cards com imagem
- **Arraste e solte** para reorganizar
- As imagens são baixadas automaticamente na primeira vez

### 4️⃣ Gerar comando
- Clique em "Gerar Comando $mm sort"
- Copie o comando gerado
- Cole no Discord: `$mm sort Personagem1 $ Personagem2 $ ...`

## Arquivos

| Arquivo | Função |
|---------|--------|
| `organizador.py` | Programa principal |
| `dados.txt` | Seus dados do Mudae (você preenche) |
| `RODAR.bat` | Atalho para rodar (Windows) |
| `imagens/` | Pasta com as imagens dos personagens (criada automaticamente) |
| `teste.py` | Script para testar se tudo funciona |

## Requisitos
- Python 3.7+
- Bibliotecas: tkinter, PIL/Pillow, requests
- Conexão com internet (para baixar imagens)

## Troubleshooting

### Erro: "dados.txt não encontrado"
- Crie um arquivo chamado `dados.txt`
- Copie o output do `$mmsaty+ri-c+x+ko` do Discord

### Imagens não aparecem
- Verifique sua conexão com a internet
- Tente rodar `python teste.py` para diagnóstico

### Programa não abre
- Tente rodar `teste.py` primeiro
- Verifique se Python está instalado: `python --version`

---

**Divirta-se organizando seus casados!** 💕
