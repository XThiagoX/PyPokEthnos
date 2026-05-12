from model.carta import Carta


class Equipe:
    """Agrupamento de cartas validas com um lider que representa
    a dominancia em uma Era"""
    def __init__(self, cartas: list[Carta], lider: Carta):
        self.membros = cartas
        self.lider = lider

    def validar_mesma_regiao_ou_tipo(self) -> bool:
        if not self.membros or self.lider not in self.membros:
            return False

        mesmo_tipo = all(
            c.tipo_pokemon == self.lider.tipo_pokemon
            for c in self.membros
        )
        mesma_regiao = all(
            c.regiao == self.lider.regiao
            for c in self.membros
        )

        return mesmo_tipo or mesma_regiao

    def tamanho_da_equipe(self) -> int:
        return len(self.membros)

    def get_regiao_lider(self) -> str:
        return self.lider.regiao
