"""Calculador de dominio e pontuacao por regiao."""
from model import Regiao


class CalculadorDominio:
    """Computa vitorias de equipe e rateios de PV nas regioes."""

    @staticmethod
    def pontos_por_tamanho(tamanho: int) -> int:
        """Escala canonica Ethnos: [1:0, 2:1, 3:3, 4:6, 5:10, 6+:15]"""
        tabela = {1: 0, 2: 1, 3: 3, 4: 6, 5: 10}
        return tabela.get(tamanho, 15)

    @staticmethod
    def tabular_fatura_de_regiao(regiao: Regiao, era_atual: int,
                                 jogadores: list) -> dict:
        """Rateia PV baseado na colocacao de acordo com o estagio da Era."""
        if not regiao.fichas_pv:
            return {}
        placar = [
            (j.nome, regiao.qtd_treinadores(j.nome))
            for j in jogadores if regiao.qtd_treinadores(j.nome) > 0
        ]
        if not placar:
            return {}

        placar.sort(key=lambda x: x[1], reverse=True)

        ganhos = {j.nome: 0 for j in jogadores}
        primeiro_colocado = placar[0]
        fichas_ativos = regiao.fichas_pv[:era_atual]
        ganhos[primeiro_colocado[0]] += (
            max(fichas_ativos) if fichas_ativos else 0
        )
        return ganhos
