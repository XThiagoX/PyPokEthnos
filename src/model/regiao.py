class Regiao:
    """Mapeamento de area que contabiliza presenca de treinadores
    e detem Fichas PV por Era"""
    def __init__(self, nome: str):
        self.nome = nome
        self.treinadores = {}  # {nome_do_jogador: int_quantidade}
        self.fichas_pv = []    # [PV Era 1, PV Era 2, PV Era 3]

    def adicionar_treinador(self, nome_jogador: str):
        if nome_jogador not in self.treinadores:
            self.treinadores[nome_jogador] = 0
        self.treinadores[nome_jogador] += 1

    def qtd_treinadores(self, nome_jogador: str) -> int:
        return self.treinadores.get(nome_jogador, 0)
