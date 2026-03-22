# Organizador Mudae - Guia de Uso

## O que é?
Um programa visual para organizar seus casados do Mudae sem digitar comandos! Funciona como o Mage Note Manager - você pode arrastar e soltar para reorganizar na ordem que quiser.

## Como usar?

### 1️⃣ Pegar os dados do Mudae
- No Discord, use o comando: `$mmsty+i-c+x+ko` (Recomendado)
- *O programa também aceita listas antigas que tenham números (ex: #123 - Nome)*
- Copie **TODO** o output (pode ser bem longo)
- Cole no arquivo `dados.txt` neste diretório

### 2️⃣ Rodar o programa
**Opção Fácil**: Clique duas vezes em `MudaeOrganizador.exe`
> *Nota: Na primeira vez, vai aparecer uma barra de carregamento baixando as imagens dos personagens. Aguarde!*

### 3️⃣ Reorganizar seus personagens
- A interface mostra todos os seus casados em cards com imagem
- **Arraste e solte** para reorganizar
- Clique com botão direito em um personagem para mudar a posição manualmente

### 4️⃣ Gerar comando
- Clique em "📋 Gerar Comando"
- Copie o comando gerado
- Cole no Discord: `$sm Personagem1 $ Personagem2 $ ...`

### 📤 Como compartilhar com amigos
Se você quer enviar o programa para alguém (sem erros de pasta .venv):
1. Execute o arquivo `COMPILAR.bat`
2. Aguarde o fim do processo
3. Uma pasta chamada `MudaOrganizador_DISTRIBUICAO` será criada automaticamente
4. **Envie essa pasta inteira** para seu amigo
   - Ela já vem pronta com o `.exe` independente e o arquivo de texto necessário.

## Arquivos

| Arquivo | Função |
|---------|--------|
| `MudaeOrganizador.exe` | **O Programa (Execute este!)** |
| `dados.txt` | Seus dados do Mudae (você preenche) |
| `imagens/` | Pasta com as imagens dos personagens (criada automaticamente) |

## Requisitos
- Se usar o `.exe`, não precisa instalar nada!
- Conexão com internet (apenas para baixar imagens na primeira vez)
- Arquivo `dados.txt` na mesma pasta do executável

## Troubleshooting

### Erro: "dados.txt não encontrado"
- Crie um arquivo chamado `dados.txt`
- Copie o output do `$mmsty+i-c+x+ko` do Discord

### Imagens não aparecem
- Verifique sua conexão com a internet
- Tente rodar `python teste.py` para diagnóstico

### Programa não abre
- Tente rodar `teste.py` primeiro
- Verifique se Python está instalado: `python --version`

---

**Divirta-se organizando seus casados!** 💕
