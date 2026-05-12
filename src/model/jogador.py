from model.carta import Carta


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
