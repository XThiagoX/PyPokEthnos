class Carta:
    """Entidade que representa uma carta no jogo PokEthnos"""
    def __init__(self, tipo_pokemon: str, area_regiao: str, eh_gatilho_fim_de_era: bool = False):
        self.tipo_pokemon = tipo_pokemon
        self.regiao = area_regiao
        self.eh_gatilho_fim_de_era = eh_gatilho_fim_de_era

    def __repr__(self):
        if self.eh_gatilho_fim_de_era:
            return "[EQUIPE ROCKET - FIM DE ERA]"
        return f"{self.tipo_pokemon} ({self.regiao})"


class Equipe:
    """Agrupamento de cartas válidas com um líder atrelado que representa a dominância em uma Era"""
    def __init__(self, cartas: list[Carta], lider: Carta):
        self.membros = cartas
        self.lider = lider

    def validar_mesma_regiao_ou_tipo(self) -> bool:
        if not self.membros or self.lider not in self.membros:
            return False
            
        mesmo_tipo = all(c.tipo_pokemon == self.lider.tipo_pokemon for c in self.membros)
        mesma_regiao = all(c.regiao == self.lider.regiao for c in self.membros)
        
        return mesmo_tipo or mesma_regiao

    def tamanho_da_equipe(self) -> int:
        return len(self.membros)
        
    def get_regiao_lider(self) -> str:
        return self.lider.regiao


class Regiao:
    """Mapeamento de área que contabiliza presença de treinadores e detém Fichas PV por Era"""
    def __init__(self, nome: str):
        self.nome = nome
        self.treinadores = {}  # {nome_do_jogador: int_quantidade}
        self.fichas_pv = []    # Ex: [PV Era 1, PV Era 2, PV Era 3] escalonado.

    def adicionar_treinador(self, nome_jogador: str):
        if nome_jogador not in self.treinadores:
            self.treinadores[nome_jogador] = 0
        self.treinadores[nome_jogador] += 1

    def qtd_treinadores(self, nome_jogador: str) -> int:
        return self.treinadores.get(nome_jogador, 0)


class Jogador:
    """Ator que joga turnos de compras ou descidas no mapa"""
    def __init__(self, nome: str):
        self.nome = nome
        self.pv = 0
        self.treinadores_disponiveis = 26
        self.mao = []
        self.equipes_baixadas = []

    def descartar_mao(self) -> list[Carta]:
        sobra = self.mao.copy()
        self.mao.clear()
        return sobra
