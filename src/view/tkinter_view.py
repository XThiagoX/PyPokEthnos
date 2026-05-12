import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from controller import (ControladorDoJogo, CARTA_VERSO_PATH,
                        MAPA_REGIOES_IMAGENS)
import os


# Tamanhos de renderizacao das cartas (pixels)
CARTA_MERCADO_W, CARTA_MERCADO_H = 70, 98
CARTA_MAO_W, CARTA_MAO_H = 85, 119
CARTA_DECK_W, CARTA_DECK_H = 70, 98

# Tamanho dos mapas de regiao
MAPA_W, MAPA_H = 200, 140


class TkinterView:
    """Frontend visual com renderizacao de sprites PNG via Pillow"""

    def __init__(self, master: tk.Tk, controller: ControladorDoJogo):
        self.root = master
        self.root.title("PokEthnos - MVP Digital")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        self.ctrl = controller

        self.selecao_indices_mao = []
        self._cache_imagens = {}  # Cache para evitar recarregar PNGs

        self._build_ui()
        self.ctrl.iniciar_nova_era()
        self.refresh()

    def _carregar_imagem(self, path: str, largura: int, altura: int):
        """Carrega, redimensiona e cacheia uma imagem PNG"""
        cache_key = (path, largura, altura)
        if cache_key in self._cache_imagens:
            return self._cache_imagens[cache_key]

        if not path or not os.path.exists(path):
            return None

        try:
            img = Image.open(path)
            img = img.resize((largura, altura), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self._cache_imagens[cache_key] = tk_img
            return tk_img
        except Exception:
            return None

    def _build_ui(self):
        # ===== HEADER =====
        self.header = tk.Frame(self.root, bg="#16213e", height=45)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)

        self.info_lbl = tk.Label(
            self.header, text="Carregando...",
            fg="#e94560", bg="#16213e",
            font=("Consolas", 11, "bold")
        )
        self.info_lbl.pack(pady=8, padx=15, side=tk.LEFT)

        self.era_lbl = tk.Label(
            self.header, text="",
            fg="#f1c40f", bg="#16213e",
            font=("Consolas", 11, "bold")
        )
        self.era_lbl.pack(pady=8, padx=15, side=tk.RIGHT)

        # ===== AREA CENTRAL (Mercado + Mapa lado a lado / empilhado) =====
        self.center_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.center_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # --- Mercado (topo) ---
        self.panel_mercado = tk.Frame(self.center_frame, bg="#0f3460", height=140)
        self.panel_mercado.pack(fill=tk.X, padx=3, pady=(2, 3))
        self.panel_mercado.pack_propagate(False)

        # --- Mapa (centro, expansivel) ---
        self.panel_map = tk.Frame(self.center_frame, bg="#1a1a2e")
        self.panel_map.pack(fill=tk.BOTH, expand=True, padx=3, pady=2)

        # ===== MAO DO JOGADOR (baixo) =====
        self.panel_mao = tk.Frame(self.root, bg="#16213e", height=190)
        self.panel_mao.pack(fill=tk.X, padx=5, pady=(2, 0))
        self.panel_mao.pack_propagate(False)

        # ===== LOG (rodape) =====
        self.log_text = tk.Text(
            self.root, height=5,
            bg="#0a0a0a", fg="#00ff41",
            font=("Consolas", 9),
            bd=0, highlightthickness=0
        )
        self.log_text.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=(0, 3))

    def refresh(self):
        jog_atual = self.ctrl.jogar_atual()

        self.info_lbl.config(
            text=(f"  Turno: {jog_atual.nome}  |  "
                  f"PV: {jog_atual.pv}  |  "
                  f"Treinadores: {jog_atual.treinadores_disponiveis}")
        )
        self.era_lbl.config(
            text=(f"Era {self.ctrl.era_atual}/{self.ctrl.max_eras}  |  "
                  f"Rockets: {self.ctrl.gatilhos_de_fim_de_era}/3  ")
        )

        self._renderizar_mercado()
        self._renderizar_mapa()
        self._renderizar_mao(jog_atual)

        # Atualizar logs
        self.log_text.delete(1.0, tk.END)
        for log in self.ctrl.log_eventos[-10:]:
            self.log_text.insert(tk.END, log + "\n")
        self.log_text.see(tk.END)

    # =========================================================================
    # MERCADO ABERTO + BARALHO
    # =========================================================================
    def _renderizar_mercado(self):
        for widget in self.panel_mercado.winfo_children():
            widget.destroy()

        container = tk.Frame(self.panel_mercado, bg="#0f3460")
        container.pack(fill=tk.BOTH, expand=True)

        # --- Baralho fechado (verso da carta) ---
        deck_frame = tk.Frame(container, bg="#0f3460")
        deck_frame.pack(side=tk.LEFT, padx=(10, 5))

        tk.Label(
            deck_frame, text="BARALHO",
            fg="#e94560", bg="#0f3460",
            font=("Consolas", 8, "bold")
        ).pack(pady=(4, 1))

        verso_img = self._carregar_imagem(
            CARTA_VERSO_PATH, CARTA_DECK_W, CARTA_DECK_H
        )
        if verso_img:
            btn_deck = tk.Button(
                deck_frame, image=verso_img,
                command=self.action_buy_deck,
                bd=2, relief=tk.RAISED,
                bg="#0f3460", activebackground="#1a1a2e",
                cursor="hand2"
            )
            btn_deck.image = verso_img
            btn_deck.pack()
        else:
            btn_deck = tk.Button(
                deck_frame,
                text=f"DECK\n({len(self.ctrl.baralho)})",
                bg="#7f8c8d", fg="white",
                command=self.action_buy_deck,
                width=9, height=5, cursor="hand2"
            )
            btn_deck.pack()

        tk.Label(
            deck_frame,
            text=f"{len(self.ctrl.baralho)} cartas",
            fg="#bdc3c7", bg="#0f3460",
            font=("Consolas", 8)
        ).pack()

        # --- Separador ---
        sep = tk.Frame(container, bg="#e94560", width=2)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=8)

        # --- Label do mercado ---
        mk_label = tk.Frame(container, bg="#0f3460")
        mk_label.pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(
            mk_label, text="M\nE\nR\nC\nA\nD\nO",
            fg="#f1c40f", bg="#0f3460",
            font=("Consolas", 8, "bold")
        ).pack(pady=5)

        # --- Cartas do mercado ---
        mercado_scroll = tk.Frame(container, bg="#0f3460")
        mercado_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for i, c in enumerate(self.ctrl.mercado_aberto):
            card_img = self._carregar_imagem(
                c.imagem_path, CARTA_MERCADO_W, CARTA_MERCADO_H
            )
            if card_img:
                btn = tk.Button(
                    mercado_scroll, image=card_img,
                    command=lambda idx=i: self.action_buy_market(idx),
                    bd=1, relief=tk.RAISED,
                    bg="#0f3460", activebackground="#16213e",
                    cursor="hand2"
                )
                btn.image = card_img
            else:
                btn = tk.Button(
                    mercado_scroll,
                    text=f"{c.nome}\n{c.tipo_pokemon}\n{c.regiao}",
                    bg="#ecf0f1", fg="#2c3e50",
                    command=lambda idx=i: self.action_buy_market(idx),
                    width=9, height=5, font=("Arial", 7),
                    cursor="hand2"
                )
            btn.pack(side=tk.LEFT, padx=2, pady=5)

    # =========================================================================
    # MAPA / TABULEIRO COM IMAGENS DE REGIAO
    # =========================================================================
    def _renderizar_mapa(self):
        for widget in self.panel_map.winfo_children():
            widget.destroy()

        # Titulo do tabuleiro
        tk.Label(
            self.panel_map,
            text="TABULEIRO CENTRAL",
            bg="#1a1a2e", fg="#f1c40f",
            font=("Consolas", 11, "bold")
        ).pack(pady=(3, 2))

        # Container: 2 fileiras de 3 regioes
        regioes_list = list(self.ctrl.mapa_regioes.items())

        row1_frame = tk.Frame(self.panel_map, bg="#1a1a2e")
        row1_frame.pack(pady=2)
        row2_frame = tk.Frame(self.panel_map, bg="#1a1a2e")
        row2_frame.pack(pady=2)

        for idx, (reg_nome, reg_obj) in enumerate(regioes_list):
            parent = row1_frame if idx < 3 else row2_frame

            # Frame da regiao
            reg_frame = tk.Frame(parent, bg="#2c2c54", bd=2, relief=tk.GROOVE)
            reg_frame.pack(side=tk.LEFT, padx=5, pady=2)

            # Imagem do mapa
            mapa_path = MAPA_REGIOES_IMAGENS.get(reg_nome, "")
            mapa_img = self._carregar_imagem(mapa_path, MAPA_W, MAPA_H)

            if mapa_img:
                mapa_lbl = tk.Label(reg_frame, image=mapa_img, bg="#2c2c54")
                mapa_lbl.image = mapa_img
                mapa_lbl.pack(padx=2, pady=(2, 0))
            else:
                # Fallback sem imagem
                tk.Label(
                    reg_frame, text=reg_nome.upper(),
                    bg="#2c2c54", fg="white",
                    font=("Consolas", 14, "bold"),
                    width=25, height=7
                ).pack(padx=2, pady=(2, 0))

            # Painel de informacoes abaixo do mapa
            info_bar = tk.Frame(reg_frame, bg="#1e1e3f")
            info_bar.pack(fill=tk.X, padx=2, pady=(0, 2))

            # Fichas PV
            fichas_str = " | ".join(str(v) for v in reg_obj.fichas_pv)
            tk.Label(
                info_bar,
                text=f"PV: [{fichas_str}]",
                fg="#f1c40f", bg="#1e1e3f",
                font=("Consolas", 8, "bold")
            ).pack(side=tk.LEFT, padx=5)

            # Treinadores presentes
            treinadores_textos = []
            for player_n, contagem in reg_obj.treinadores.items():
                if contagem > 0:
                    nome_curto = player_n.split()[0]
                    treinadores_textos.append(f"{nome_curto}:{contagem}")

            if treinadores_textos:
                tk.Label(
                    info_bar,
                    text="  ".join(treinadores_textos),
                    fg="#2ecc71", bg="#1e1e3f",
                    font=("Consolas", 8, "bold")
                ).pack(side=tk.RIGHT, padx=5)

    # =========================================================================
    # MAO DO JOGADOR
    # =========================================================================
    def _renderizar_mao(self, jogador):
        for widget in self.panel_mao.winfo_children():
            widget.destroy()

        self.selecao_indices_mao.clear()

        # Header da mao
        header_mao = tk.Frame(self.panel_mao, bg="#16213e")
        header_mao.pack(fill=tk.X, pady=(4, 2))

        tk.Label(
            header_mao,
            text=(f"  MAO DE {jogador.nome.upper()}  "
                  f"({len(jogador.mao)}/10)  -  "
                  f"1a carta selecionada = Lider"),
            fg="white", bg="#16213e",
            font=("Consolas", 9)
        ).pack(side=tk.LEFT, padx=10)

        # Botao de baixar equipe
        btn_jogar = tk.Button(
            header_mao,
            text="BAIXAR EQUIPE",
            bg="#e94560", fg="white",
            font=("Consolas", 10, "bold"),
            command=self.action_play_team,
            padx=15, pady=2,
            cursor="hand2",
            activebackground="#c0392b"
        )
        btn_jogar.pack(side=tk.RIGHT, padx=10)

        # Container de cartas da mao
        cards_frame = tk.Frame(self.panel_mao, bg="#16213e")
        cards_frame.pack(fill=tk.X, padx=10, pady=3)

        card_frames = {}

        def atualizar_estilos_selecao():
            for card_frame in card_frames.values():
                card_frame.config(bg="#16213e", bd=2)

            if not self.selecao_indices_mao:
                return

            idx_lider = self.selecao_indices_mao[0]
            if idx_lider in card_frames:
                card_frames[idx_lider].config(bg="#f1c40f", bd=4)

            for idx in self.selecao_indices_mao[1:]:
                if idx in card_frames:
                    card_frames[idx].config(bg="#bdc3c7", bd=3)

        def toggle_selection(idx):
            if idx in self.selecao_indices_mao:
                self.selecao_indices_mao.remove(idx)
            else:
                self.selecao_indices_mao.append(idx)
            atualizar_estilos_selecao()

        for i, c in enumerate(jogador.mao):
            card_container = tk.Frame(
                cards_frame, bg="#16213e",
                bd=2, relief=tk.RAISED
            )
            card_container.pack(side=tk.LEFT, padx=3, pady=2)
            card_frames[i] = card_container

            card_img = self._carregar_imagem(
                c.imagem_path, CARTA_MAO_W, CARTA_MAO_H
            )

            if card_img:
                btn = tk.Button(
                    card_container, image=card_img,
                    bd=0, relief=tk.FLAT,
                    bg="#16213e", activebackground="#0f3460",
                    cursor="hand2"
                )
                btn.image = card_img
                btn.config(
                    command=lambda idx=i: toggle_selection(idx)
                )
                btn.pack()
            else:
                btn = tk.Button(
                    card_container,
                    text=f"{c.nome}\n{c.tipo_pokemon}\n{c.regiao}",
                    bg="#ecf0f1", fg="#2c3e50",
                    width=11, height=5, font=("Arial", 8),
                    cursor="hand2"
                )
                btn.config(
                    command=lambda idx=i: toggle_selection(idx)
                )
                btn.pack()

            # Nome abaixo da carta
            tk.Label(
                card_container,
                text=c.nome[:12] if c.nome else c.tipo_pokemon,
                fg="#bdc3c7", bg="#16213e",
                font=("Consolas", 7)
            ).pack()

    # =========================================================================
    # ACTIONS
    # =========================================================================
    def action_buy_deck(self):
        if self.ctrl.era_atual > self.ctrl.max_eras:
            return
        ok, msg = self.ctrl.comprar_carta_do_baralho(self.ctrl.jogar_atual())
        if not ok:
            messagebox.showwarning("Proibido", msg)
        self.refresh()

    def action_buy_market(self, idx):
        if self.ctrl.era_atual > self.ctrl.max_eras:
            return
        ok, msg = self.ctrl.comprar_carta_do_mercado(
            self.ctrl.jogar_atual(), idx
        )
        if not ok:
            messagebox.showwarning("Proibido", msg)
        self.refresh()

    def action_play_team(self):
        if self.ctrl.era_atual > self.ctrl.max_eras:
            return
        if not self.selecao_indices_mao:
            messagebox.showinfo(
                "Cuidado",
                "Selecione cartas da sua mao clicando nelas."
            )
            return

        idx_lider = self.selecao_indices_mao[0]
        ok, msg = self.ctrl.jogar_equipe(
            self.ctrl.jogar_atual(),
            self.selecao_indices_mao,
            idx_lider
        )

        if not ok:
            messagebox.showerror("Regra do Jogo Violada", msg)
        self.refresh()
