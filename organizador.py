import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import re
import requests
import os
import json

# --- CONFIGURAÇÕES ---
DADOS_FILE = "dados.txt"
IMGS_FOLDER = "imagens"
FINAL_ORDER_FILE = "ordem_final.json"
colunas_grade = 10
CARD_WIDTH = 110
CARD_HEIGHT = 150

# Cria a pasta de imagens se não existir
if not os.path.exists(IMGS_FOLDER):
    os.makedirs(IMGS_FOLDER)

# --- 1. FUNÇÃO DE PARSE E DOWNLOAD (The "Mage") ---
def carregar_e_baixar_dados():
    if not os.path.exists(DADOS_FILE):
        messagebox.showerror("Erro", "Crie um arquivo dados.txt com o output do comando $mmsaty+ri-c+x+ko")
        return {}

    with open(DADOS_FILE, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Regex para capturar ID, Nome e URL (Padrão 1 - Com ID de Rank)
    # Exemplo: **#5.523** - Misuzu Gundou  💞 => ... <URL>
    padrao = re.compile(r"\*?\*?#([\d.]+)\*?\*?\s*-\s*([^💞]+)\s*💞.*?(https?://[^\s>]+)", re.DOTALL)
    matches = padrao.findall(texto)
    
    # Se não encontrar nada, tenta o Padrão 2 (Sem ID de Rank, gerado por outro comando)
    # Exemplo: Mai Sakurajima  💞 => matheus_reptil · ($wa) 1.035 ka - https://...
    if not matches:
        padrao_alt = re.compile(r"^\s*\*?\*?([^💞\n]+?)\*?\*?\s*💞.*?(https?://[^\s>]+)", re.MULTILINE)
        matches_alt = padrao_alt.findall(texto)
        # Como o Padrão 2 não possui ID, vamos usar a posição na lista (1, 2, 3...) como ID
        matches = [(str(i), nome, url) for i, (nome, url) in enumerate(matches_alt, start=1)]

    personagens = {}
    for match in matches:
        char_id = match[0].replace('.', '_')  # Converter 5.523 → 5_523 para ser chave válida
        char_name = match[1].strip()
        img_url = match[2].strip()
        
        personagens[char_id] = {'nome': char_name, 'url': img_url, 'id_original': match[0]}
        
        # Download da imagem se não existir
        img_path = os.path.join(IMGS_FOLDER, f"{char_id}.jpg")
        if not os.path.exists(img_path):
            print(f"Baixando imagem de {char_name}...")
            try:
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(img_path, 'wb') as f_img:
                        for chunk in response.iter_content(1024):
                            f_img.write(chunk)
            except Exception as e:
                print(f"Erro ao baixar {char_name}: {e}")

    return personagens

# --- 2. CLASSE DO CARD COM BARRA DE INFORMAÇÕES ---
class GalleryCardV2(tk.Frame):
    def __init__(self, parent, app, char_id, char_data, image, position, **kwargs):
        super().__init__(parent, bg="#1a1a1a", relief="ridge", bd=1, width=120, height=160, **kwargs)
        self.char_id = char_id
        self.char_data = char_data
        self.app = app
        self.selected = False
        self.pack_propagate(False)
        
        # --- IMAGEM (maior) ---
        img_frame = tk.Frame(self, bg="#1a1a1a")
        img_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.img_label = tk.Label(img_frame, image=image, bg="#1a1a1a", cursor="hand2")
        self.img_label.pack(fill="both", expand=True)
        self.photo = image
        
        # Badge de Posição
        self.rank_badge = tk.Label(
            img_frame,
            text=f"#{position + 1}",
            bg="#FF69B4",
            fg="white",
            font=("Arial", 8, "bold"),
            padx=3,
            pady=0
        )
        self.rank_badge.place(x=0, y=0)
        
        # --- BARRA DE DADOS EMBAIXO ---
        info_frame = tk.Frame(self, bg="#000000", height=45)
        info_frame.pack(fill="x", side="bottom")
        info_frame.pack_propagate(False)
        
        # Nome (grande)
        name_label = tk.Label(
            info_frame,
            text=char_data['nome'][:13],
            bg="#000000",
            fg="white",
            font=("Arial", 8, "bold"),
            justify="center",
            wraplength=115
        )
        name_label.pack(fill="x", padx=2, pady=2)
        
        # ID (pequeno)
        id_label = tk.Label(
            info_frame,
            text=f"ID: {char_data['id_original']}",
            bg="#000000",
            fg="#88ff00",
            font=("Arial", 7),
            justify="center"
        )
        id_label.pack(fill="x", padx=2, pady=0)
        
        # Eventos
        for widget in [self, self.img_label, img_frame, info_frame, name_label, id_label, self.rank_badge]:
            widget.bind("<ButtonPress-1>", self._on_press)
            widget.bind("<B1-Motion>", self._on_motion)
            widget.bind("<ButtonRelease-1>", self._on_release)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-3>", self._on_right_click)
            
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False
    
    def _on_press(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._is_dragging = False
        
    def _on_motion(self, event):
        if not self._is_dragging:
            if abs(event.x - self._drag_start_x) > 5 or abs(event.y - self._drag_start_y) > 5:
                self._is_dragging = True
                self.app.start_drag(self)
        if self._is_dragging:
            self.app.update_drag()
    
    def _on_release(self, event):
        if self._is_dragging:
            self.app.stop_drag()
            self._is_dragging = False
        else:
            self.app.selecionar_card(self.char_id, self)

    def _on_right_click(self, event):
        self.app.show_context_menu(event, self.char_id)

    def _on_enter(self, event):
        if not self.selected:
            self.config(bg="#2a2a2a", relief="sunken")
    
    def _on_leave(self, event):
        if not self.selected:
            self.config(bg="#1a1a1a", relief="ridge")
    
    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.config(bg="#FF69B4", relief="sunken", bd=2)
        else:
            self.config(bg="#1a1a1a", relief="ridge", bd=1)
            
    def update_position(self, position):
        self.rank_badge.config(text=f"#{position + 1}")


# --- 3. CLASSE PRINCIPAL DA INTERFACE (Estilo Mudae Note Manager) ---
class MudaeOrganizador:
    def __init__(self, root, personagens):
        self.root = root
        self.root.title("Mudae Note Manager - Organizador Casados")
        self.root.geometry("1500x900")
        self.root.configure(bg="#0d0d0d")
        
        self.personagens = personagens
        self.ordem_ids = list(personagens.keys())
        self.selected_card = None
        self.cards = {}
        
        self.drag_window = None
        self.drag_source = None
        self.drag_target = None
        
        # === DIVISÃO PRINCIPAL ===
        # TOP FRAME (com 3 painéis: Input, Options, Ranking)
        top_frame = tk.Frame(root, bg="#0d0d0d", height=300)
        top_frame.pack(fill="x", side="top", padx=5, pady=5)
        top_frame.pack_propagate(False)
        
        # --- PAINEL ESQUERDO (INPUT) ---
        left_panel = tk.LabelFrame(top_frame, text="Input", bg="#1a1a1a", fg="#FF69B4", 
                                    font=("Arial", 10, "bold"), padx=10, pady=10)
        left_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        input_frame = tk.Frame(left_panel, bg="#1a1a1a")
        input_frame.pack(fill="both", expand=True)
        
        input_text = tk.Text(input_frame, height=12, width=30, bg="#0d0d0d", fg="#00ff00", 
                            font=("Courier", 8), wrap="word")
        input_text.insert("1.0", "# Total de Casados:\n# " + str(len(self.ordem_ids)) + "\n\n# Personagens carregados:")
        input_text.config(state="disabled")
        input_text.pack(fill="both", expand=True)
        
        # --- PAINEL CENTRAL (OPTIONS) ---
        mid_panel = tk.LabelFrame(top_frame, text="Options", bg="#1a1a1a", fg="#FF69B4",
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        mid_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        # Seção SORTING
        sort_lbl = tk.Label(mid_panel, text="SORTING & DISPLAY", bg="#1a1a1a", fg="#FF69B4", 
                           font=("Arial", 9, "bold"))
        sort_lbl.pack(anchor="w", pady=(0, 5))
        
        sort_btnframe = tk.Frame(mid_panel, bg="#1a1a1a")
        sort_btnframe.pack(fill="x", padx=5)
        
        # Botões de Ordenação Funcionais
        btn_rank = tk.Button(sort_btnframe, text="Rank", command=self.sort_rank,
                            bg="#7C3AED", fg="white", font=("Arial", 8), padx=8, pady=3)
        btn_rank.pack(side="left", padx=2)
        
        btn_az = tk.Button(sort_btnframe, text="A-Z", command=self.sort_az,
                          bg="#7C3AED", fg="white", font=("Arial", 8), padx=8, pady=3)
        btn_az.pack(side="left", padx=2)
        
        # Seção FILTERING
        filter_lbl = tk.Label(mid_panel, text="FILTERING", bg="#1a1a1a", fg="#FF69B4",
                             font=("Arial", 9, "bold"))
        filter_lbl.pack(anchor="w", pady=(10, 5))
        
        # Botão Gerar Comando em destaque
        btn_gerar = tk.Button(mid_panel, text="📋 Gerar Comando", command=self.gerar_comando,
                             bg="#FF69B4", fg="white", font=("Arial", 10, "bold"), 
                             padx=15, pady=8)
        btn_gerar.pack(fill="x", pady=(10, 0))
        
        # --- PAINEL DIREITO (RANKING/STATS) ---
        right_panel = tk.LabelFrame(top_frame, text="uft", bg="#1a1a1a", fg="#FF69B4",
                                    font=("Arial", 10, "bold"), padx=10, pady=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=5)
        
        stats_text = tk.Text(right_panel, height=12, width=20, bg="#0d0d0d", fg="#FF69B4",
                            font=("Courier", 8), wrap="word")
        stats_text.insert("1.0", f"Total Casados:\n{len(self.ordem_ids)}\n\n")
        stats_text.insert("end", "Total Únicos:\n" + str(len(self.ordem_ids)))
        stats_text.config(state="disabled")
        stats_text.pack(fill="both", expand=True)
        
        # === FRAME INFERIOR (GALERIA) ===
        bottom_frame = tk.Frame(root, bg="#0d0d0d")
        bottom_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Label "All Characters"
        gallery_title = tk.Label(bottom_frame, text="All Characters", bg="#0d0d0d", fg="#FF69B4",
                                font=("Arial", 11, "bold"))
        gallery_title.pack(anchor="w", pady=(0, 5))
        
        # Canvas com scrollbar VERTICAL
        self.canvas = tk.Canvas(bottom_frame, bg="#0d0d0d", highlightthickness=0)
        scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0d0d0d")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel vertical
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.root.bind("<MouseWheel>", _on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # === CARREGAR IMAGENS ===
        self.tk_images = {}
        for i, char_id in enumerate(self.ordem_ids):
            img_path = os.path.join(IMGS_FOLDER, f"{char_id}.jpg")
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img = img.resize((CARD_WIDTH, CARD_HEIGHT - 50), Image.Resampling.LANCZOS)
                    self.tk_images[char_id] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Erro ao carregar {char_id}: {e}")
        
        self.desenhar_galeria()

    # --- FUNÇÕES DE ORDENAÇÃO ---
    def sort_rank(self):
        # Ordena pelo ID original (Rank). Remove pontos de milhar (ex: 17.736 -> 17736)
        def get_rank(char_id):
            try:
                raw_id = self.personagens[char_id]['id_original'].replace('.', '')
                return int(raw_id)
            except ValueError:
                return 999999
        
        self.ordem_ids.sort(key=get_rank)
        self.desenhar_galeria()

    def sort_az(self):
        # Ordena alfabeticamente pelo nome
        self.ordem_ids.sort(key=lambda x: self.personagens[x]['nome'].lower())
        self.desenhar_galeria()
    
    def desenhar_galeria(self):
        # Otimização: Reutilizar widgets existentes em vez de destruir e recriar
        row = 0
        col = 0
        
        for i, char_id in enumerate(self.ordem_ids):
            if char_id not in self.tk_images:
                continue
                
            if char_id in self.cards:
                # Atualizar card existente
                card = self.cards[char_id]
                card.update_position(i)
            else:
                # Criar novo card se não existir
                char_data = self.personagens[char_id]
                card = GalleryCardV2(
                    self.scrollable_frame,
                    self,
                    char_id,
                    char_data,
                    self.tk_images[char_id],
                    i
                )
                self.cards[char_id] = card
            
            # Apenas reposiciona na grade (muito mais rápido que recriar)
            card.grid(row=row, column=col, padx=3, pady=3)
            
            col += 1
            if col >= colunas_grade:
                col = 0
                row += 1

    # --- DRAG AND DROP ---
    def start_drag(self, card):
        self.drag_source = card
        self.drag_target = None
        
        # Criar janela fantasma (Ghost Image)
        self.drag_window = tk.Toplevel(self.root)
        self.drag_window.overrideredirect(True)
        self.drag_window.attributes('-topmost', True)
        self.drag_window.attributes('-alpha', 0.7)
        
        # Label com a imagem do card arrastado
        lbl = tk.Label(self.drag_window, image=card.photo, bg='black', bd=2, relief="solid")
        lbl.pack()
        
        self.update_drag()
    
    def update_drag(self):
        if self.drag_window:
            x, y = self.root.winfo_pointerxy()
            # Posiciona levemente deslocado para não interferir no clique
            self.drag_window.geometry(f"+{x+15}+{y+15}")
            self.check_scroll(y)
            
            # Identificar e destacar o alvo
            target_card = self._get_card_under_mouse(x, y)
            
            # Remove destaque do alvo anterior se mudou
            if self.drag_target and self.drag_target != target_card and self.drag_target != self.drag_source:
                 # Restaura cor original (ou de selecionado)
                 if self.drag_target.char_id == self.selected_card:
                     self.drag_target.config(bg="#FF69B4", relief="sunken")
                 else:
                     self.drag_target.config(bg="#1a1a1a", relief="ridge")
            
            # Destaca novo alvo
            if target_card and target_card != self.drag_source:
                target_card.config(bg="#00ffff", relief="solid", bd=2)
                self.drag_target = target_card
            else:
                self.drag_target = None

    def check_scroll(self, y_root):
        # Auto scroll ao arrastar perto das bordas
        canvas_y = self.canvas.winfo_rooty()
        canvas_height = self.canvas.winfo_height()
        
        if y_root < canvas_y + 50:
            self.canvas.yview_scroll(-1, "units")
        elif y_root > canvas_y + canvas_height - 50:
            self.canvas.yview_scroll(1, "units")
            
    def stop_drag(self):
        if self.drag_window:
            self.drag_window.destroy()
            self.drag_window = None
        
        # Limpar destaque visual do alvo
        if self.drag_target:
            if self.drag_target.char_id == self.selected_card:
                self.drag_target.config(bg="#FF69B4", relief="sunken")
            else:
                self.drag_target.config(bg="#1a1a1a", relief="ridge")

        # Realizar a troca se houver alvo válido
        if self.drag_target and self.drag_target != self.drag_source:
            self.mover_personagem(self.drag_source.char_id, self.drag_target.char_id)

    def _get_card_under_mouse(self, x, y):
        widget = self.root.winfo_containing(x, y)
        curr = widget
        while curr:
            if isinstance(curr, GalleryCardV2):
                return curr
            curr = curr.master
        return None
            
    def mover_personagem(self, id_origem, id_destino):
        idx_origem = self.ordem_ids.index(id_origem)
        
        # Remove da posição antiga
        self.ordem_ids.pop(idx_origem)
        
        # Descobre a nova posição do alvo (pode ter mudado após o pop)
        idx_destino_novo = self.ordem_ids.index(id_destino)
        
        # Insere na posição do alvo (empurrando o alvo para frente)
        self.ordem_ids.insert(idx_destino_novo, id_origem)
        
        self.desenhar_galeria()

    # --- MENU DE CONTEXTO ---
    def show_context_menu(self, event, char_id):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🔢 Mudar Posição (#)", command=lambda: self.ask_posicao(char_id))
        menu.tk_popup(event.x_root, event.y_root)

    def ask_posicao(self, char_id):
        current_pos = self.ordem_ids.index(char_id) + 1
        new_pos = simpledialog.askinteger("Mudar Posição", 
                                        f"Atual: {current_pos}\nNova posição (1-{len(self.ordem_ids)}):",
                                        parent=self.root,
                                        minvalue=1,
                                        maxvalue=len(self.ordem_ids))
        if new_pos is not None:
            # Ajustar index (usuário vê 1-N, lista é 0-N)
            target_index = new_pos - 1
            self.ordem_ids.pop(self.ordem_ids.index(char_id))
            self.ordem_ids.insert(target_index, char_id)
            self.desenhar_galeria()
    
    def selecionar_card(self, char_id, card):
        # Desselecionar anterior
        if self.selected_card and self.selected_card in self.cards:
            self.cards[self.selected_card].set_selected(False)
        
        # Selecionar novo
        self.selected_card = char_id
        card.set_selected(True)
    
    def gerar_comando(self):
        nomes_ordenados = []
        for char_id in self.ordem_ids:
            nomes_ordenados.append(self.personagens[char_id]['nome'])
        
        if len(nomes_ordenados) == 0:
            messagebox.showwarning("Aviso", "Nenhum personagem encontrado!")
            return
        
        comando_final = "$sm " + " $ ".join(nomes_ordenados)
        
        # Janela de resultado
        janela = tk.Toplevel(self.root)
        janela.title("Comando Gerado")
        janela.geometry("1000x400")
        janela.configure(bg="#0d0d0d")
        
        # Header
        header = tk.Frame(janela, bg="#1a1a1a")
        header.pack(fill="x", padx=10, pady=10)
        
        info = tk.Label(header, text=f"✓ Comando com {len(nomes_ordenados)} personagens",
                       bg="#1a1a1a", fg="#FF69B4", font=("Arial", 11, "bold"))
        info.pack()
        
        # Texto do comando
        txt_frame = tk.Frame(janela, bg="#0d0d0d")
        txt_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        txt_area = tk.Text(txt_frame, height=12, bg="#0d0d0d", fg="#FF69B4", 
                          font=("Courier", 10), wrap="word")
        txt_area.insert("1.0", comando_final)
        txt_area.config(state="disabled")
        
        scrollbar_txt = ttk.Scrollbar(txt_frame, orient="vertical", command=txt_area.yview)
        txt_area.configure(yscrollcommand=scrollbar_txt.set)
        
        txt_area.pack(side="left", fill="both", expand=True)
        scrollbar_txt.pack(side="right", fill="y")
        
        # Botão copiar
        btn_frame = tk.Frame(janela, bg="#0d0d0d")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        btn_copy = tk.Button(btn_frame, text="📋 Copiar Comando", 
                            command=lambda: self._copiar(comando_final, janela),
                            bg="#FF69B4", fg="white", font=("Arial", 11, "bold"),
                            padx=20, pady=8)
        btn_copy.pack(side="left")
        
        btn_close = tk.Button(btn_frame, text="Fechar", command=janela.destroy,
                             bg="#666", fg="white", font=("Arial", 10),
                             padx=15, pady=8)
        btn_close.pack(side="right")
    
    def _copiar(self, texto, janela):
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        messagebox.showinfo("Copiado!", 
                           "✓ Comando copiado com sucesso!\n\n"
                           "Agora cole no Discord.\n(O comando já inclui o $sm)", parent=janela)



# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    # Passo 1: Processar e Baixar
    dados_carregados = carregar_e_baixar_dados()
    
    if dados_carregados:
        # Passo 2: Iniciar Interface
        root = tk.Tk()
        # Ajustar tamanho inicial
        root.geometry("800x600")
        app = MudaeOrganizador(root, dados_carregados)
        root.mainloop()
    elif os.path.exists(DADOS_FILE):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", "Nenhum personagem encontrado!\n\nO arquivo dados.txt existe, mas o formato não foi reconhecido.\nVerifique se copiou o output correto do Mudae.")
        root.destroy()