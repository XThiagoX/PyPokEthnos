import tkinter as tk
from tkinter import messagebox
from controllers import ControladorDoJogo

class TkinterView:
    """Implementa o frontend visual para testagem das interações em Pass-And-Play Loop"""
    def __init__(self, master: tk.Tk, controller: ControladorDoJogo):
        self.root = master
        self.root.title("PokEthnos Visual MVP")
        self.root.geometry("1400x850")
        self.root.configure(bg="#2c3e50")
        self.ctrl = controller
        
        self.selecao_indices_mao = [] # Hold selected cards from hand to build teams
        
        self._build_ui()
        self.ctrl.iniciar_nova_era()
        self.refresh()

    def _build_ui(self):
        # Top Panel: Market and Info
        self.panel_top = tk.Frame(self.root, bg="#34495e", height=150)
        self.panel_top.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_lbl = tk.Label(self.panel_top, text="Carregando...", fg="white", bg="#34495e", font=("Arial", 14, "bold"))
        self.info_lbl.pack(pady=5)
        
        # Center: Regions and Map
        self.panel_map = tk.Frame(self.root, bg="#1abc9c", height=300)
        self.panel_map.pack(fill=tk.X, padx=10, pady=5)
        
        # Bottom: Player Hand
        self.panel_bottom = tk.Frame(self.root, bg="#34495e", height=200)
        self.panel_bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(self.root, height=8, bg="black", fg="#00FF00", font=("Consolas", 10))
        self.log_text.pack(fill=tk.X, side=tk.BOTTOM)
        
    def refresh(self):
        jog_atual = self.ctrl.jogar_atual()
        self.info_lbl.config(text=f"PokEthnos | Era {self.ctrl.era_atual}/{self.ctrl.max_eras} | Turno de: {jog_atual.nome} | PVs: {jog_atual.pv} | Treinadores em estoque: {jog_atual.treinadores_disponiveis}\nEquipe Rockets Compradas: {self.ctrl.gatilhos_de_fim_de_era}/3")
        
        self._renderizar_mercado()
        self._renderizar_mapa()
        self._renderizar_mao(jog_atual)
        
        # Update logs
        self.log_text.delete(1.0, tk.END)
        for log in self.ctrl.log_eventos[-15:]:
            self.log_text.insert(tk.END, log + "\n")
        self.log_text.see(tk.END)

    def _renderizar_mercado(self):
        for widget in self.panel_top.winfo_children():
            if widget != self.info_lbl: widget.destroy()
            
        btn_deck = tk.Button(self.panel_top, text=f"📥 COMPRAR DECK\n({len(self.ctrl.baralho)} cart.)", bg="#7f8c8d", fg="white",
                             command=self.action_buy_deck, width=15, height=4)
        btn_deck.pack(side=tk.LEFT, padx=20)
        
        for i, c in enumerate(self.ctrl.mercado_aberto):
            btn = tk.Button(self.panel_top, text=f"{c.tipo_pokemon}\n{c.regiao}", bg="#ecf0f1",
                            command=lambda idx=i: self.action_buy_market(idx), width=10, height=4)
            btn.pack(side=tk.LEFT, padx=5)

    def _renderizar_mapa(self):
        for widget in self.panel_map.winfo_children(): widget.destroy()
        tk.Label(self.panel_map, text="🗺 REGIONS DO TABULEIRO CENTRAL 🗺", bg="#1abc9c", fg="white", font=("Arial", 12, "bold")).pack(pady=2)
        
        map_container = tk.Frame(self.panel_map, bg="#1abc9c")
        map_container.pack()
        
        for reg_nome, reg_obj in self.ctrl.mapa_regioes.items():
            f = tk.Frame(map_container, bg="#16a085", bd=2, relief=tk.RAISED, width=150, height=150)
            f.pack_propagate(False)
            f.pack(side=tk.LEFT, padx=10, pady=10)
            tk.Label(f, text=reg_nome.upper(), bg="#16a085", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            
            fichas = [str(v) for v in reg_obj.fichas_pv]
            tk.Label(f, text="PVs: [" + " | ".join(fichas) + "]", bg="#16a085", fg="#f1c40f").pack()
            
            for player_n, contagem in reg_obj.treinadores.items():
                if contagem > 0:
                    tk.Label(f, text=f"{player_n}: {contagem} peças", bg="#16a085", fg="black").pack()

    def _renderizar_mao(self, jogador):
        for widget in self.panel_bottom.winfo_children(): widget.destroy()
        
        tk.Label(self.panel_bottom, text="🃏 SUA MÃO (Selecione cartas para agrupar e formar Equipe, o primeiro clique será o líder) 🃏", bg="#34495e", fg="white").pack(pady=5)
        
        cards_frame = tk.Frame(self.panel_bottom, bg="#34495e")
        cards_frame.pack()
        
        self.selecao_indices_mao.clear() # Reset selection on new render
        
        def toggle_selection(btn, idx):
            if idx in self.selecao_indices_mao:
                self.selecao_indices_mao.remove(idx)
                btn.config(bg="#ecf0f1", relief=tk.RAISED)
            else:
                self.selecao_indices_mao.append(idx)
                if len(self.selecao_indices_mao) == 1:
                    btn.config(bg="#f1c40f", relief=tk.SUNKEN) # Leader
                else:
                    btn.config(bg="#bdc3c7", relief=tk.SUNKEN) # Group
                
        for i, c in enumerate(jogador.mao):
            b = tk.Button(cards_frame, text=f"{c.tipo_pokemon}\n{c.regiao}", bg="#ecf0f1", width=12, height=6)
            b.config(command=lambda btn=b, idx=i: toggle_selection(btn, idx))
            b.pack(side=tk.LEFT, padx=5, pady=15)
            
        btn_jogar = tk.Button(self.panel_bottom, text="⚔ BAIXAR EQUIPE COM A SELEÇÃO ⚔", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), command=self.action_play_team)
        btn_jogar.pack(pady=10)

    def action_buy_deck(self):
        if self.ctrl.era_atual > self.ctrl.max_eras: return
        ok, msg = self.ctrl.comprar_carta_do_baralho(self.ctrl.jogar_atual())
        if not ok: messagebox.showwarning("Proibido", msg)
        self.refresh()

    def action_buy_market(self, idx):
        if self.ctrl.era_atual > self.ctrl.max_eras: return
        ok, msg = self.ctrl.comprar_carta_do_mercado(self.ctrl.jogar_atual(), idx)
        if not ok: messagebox.showwarning("Proibido", msg)
        self.refresh()
        
    def action_play_team(self):
        if self.ctrl.era_atual > self.ctrl.max_eras: return
        if not self.selecao_indices_mao:
            messagebox.showinfo("Cuidado", "Selecione cartas da sua mão clicando nelas.")
            return
            
        # O Líder é fisicamente a 1ª carta que ele clicou da sub-lista gerada
        idx_lider = self.selecao_indices_mao[0] 
        ok, msg = self.ctrl.jogar_equipe(self.ctrl.jogar_atual(), self.selecao_indices_mao, idx_lider)
        
        if not ok:
            messagebox.showerror("Regra do Jogo Violada", msg)
        self.refresh()
