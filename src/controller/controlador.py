"""Controlador principal do fluxo de jogo PokEthnos."""
import random
from model import Carta, Jogador, Regiao, Equipe
from controller.calculador import CalculadorDominio
from controller.assets_config import (
    POKEMON_MAPA, ROCKET_IMAGENS, resolver_imagem_path
)


class ControladorDoJogo:
    """Orquestra o fluxo de turnos, eras e pontuacao do jogo."""

    def __init__(self):
        self.era_atual = 1
        self.max_eras = 2  # Setup para 2 Players Pass-And-Play
        self.gatilhos_de_fim_de_era = 0

        self.jogadores = [Jogador("Ash Ketchum"), Jogador("Gary Oak")]
        self.turno_atual = 0

        self.tipos_ativos = [
            "Planta", "Fogo", "Água", "Pedra", "Psíquico", "Lutador"
        ]
        self.regioes_nomes = [
            "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos"
        ]

        self.mapa_regioes = {
            nome: Regiao(nome) for nome in self.regioes_nomes
        }

        # Forjamento Base das fichas aleatorias
        for r in self.mapa_regioes.values():
            r.fichas_pv = sorted([
                random.randint(1, 3),
                random.randint(4, 7),
                random.randint(8, 10)
            ])

        self.baralho = []
        self.mercado_aberto = []
        self.log_eventos = []

    def add_log(self, text):
        self.log_eventos.append(text)

    def jogar_atual(self) -> Jogador:
        return self.jogadores[self.turno_atual]

    def passar_turno(self):
        self.turno_atual = (self.turno_atual + 1) % len(self.jogadores)
        self.add_log(f"Turno passado para {self.jogar_atual().nome}")

    def iniciar_nova_era(self):
        self.add_log(f"--- INICIO DA ERA {self.era_atual} ---")
        self.gatilhos_de_fim_de_era = 0
        self.baralho.clear()
        self.mercado_aberto.clear()

        for j in self.jogadores:
            j.mao.clear()
            j.equipes_baixadas.clear()

        # Povoar baralho com a combinatoria dos Tipos vs Regioes
        cartas_base = []
        for t in self.tipos_ativos:
            for r in self.regioes_nomes:
                dados = POKEMON_MAPA.get(r, {}).get(t)
                if dados:
                    nome_pokemon, arquivo_base = dados
                    img_path = resolver_imagem_path(t, arquivo_base)
                else:
                    nome_pokemon = f"{t} Desconhecido"
                    img_path = ""
                cartas_base.append(Carta(t, r, nome=nome_pokemon,
                                        imagem_path=img_path))
                cartas_base.append(Carta(t, r, nome=nome_pokemon,
                                        imagem_path=img_path))

        random.shuffle(cartas_base)

        # Sacar 1 pra Mao e Abrir Mercado
        for j in self.jogadores:
            j.mao.append(cartas_base.pop())

        for _ in range(2 * len(self.jogadores)):
            self.mercado_aberto.append(cartas_base.pop())

        # Insercao das cartas Equipe Rocket na metade inferior do deck
        ponto_corte = len(cartas_base) // 2
        metade_fundo = cartas_base[:ponto_corte]
        metade_topo = cartas_base[ponto_corte:]

        for i in range(3):
            metade_fundo.append(Carta(
                "Equipe Rocket", "N/A",
                nome="Equipe Rocket",
                imagem_path=ROCKET_IMAGENS[i],
                eh_gatilho_fim_de_era=True
            ))

        random.shuffle(metade_fundo)
        self.baralho = metade_fundo + metade_topo

    def comprar_carta_do_baralho(self, jogador: Jogador):
        if len(jogador.mao) >= 10:
            return False, "Sua Mao possui Limite de 10 Cartas (RF04)."

        if not self.baralho:
            return False, "Baralho Mestre esvaziado."

        carta = self.baralho.pop()

        if carta.eh_gatilho_fim_de_era:
            self.gatilhos_de_fim_de_era += 1
            self.add_log(
                f"EQUIPE ROCKET REVELADA! "
                f"({self.gatilhos_de_fim_de_era}/3)"
            )
            if self.gatilhos_de_fim_de_era >= 3:
                self.encerrar_era_e_contar_pv()
                return True, "FIM DE ERA ATIVADO!"
            else:
                return self.comprar_carta_do_baralho(jogador)

        jogador.mao.append(carta)
        self.add_log(f"{jogador.nome} comprou {carta} da Nuvem Fechada.")
        self.passar_turno()
        return True, "Compra consolidada."

    def comprar_carta_do_mercado(self, jogador: Jogador, index: int):
        if len(jogador.mao) >= 10:
            return False, "Sua Mao possui Limite de 10 Cartas."
        if index < 0 or index >= len(self.mercado_aberto):
            return False, "Carta Inexistente."

        carta = self.mercado_aberto.pop(index)
        jogador.mao.append(carta)
        self.add_log(f"{jogador.nome} pescou do mercado {carta}.")
        self.passar_turno()
        return True, "Operacao Comercial realizada."

    def jogar_equipe(self, jogador: Jogador, indices_cartas: list[int],
                     index_lider: int):
        cartas = [jogador.mao[i] for i in indices_cartas]
        lider = jogador.mao[index_lider]

        equipe = Equipe(cartas, lider)
        if not equipe.validar_mesma_regiao_ou_tipo():
            return False, ("Sintaxe da Equipe Recusada! "
                           "Exige Coesao de Tipo ou Regiao.")

        regiao = self.mapa_regioes[equipe.get_regiao_lider()]

        txt_adicional = ""
        if equipe.tamanho_da_equipe() > regiao.qtd_treinadores(jogador.nome):
            if jogador.treinadores_disponiveis > 0:
                regiao.adicionar_treinador(jogador.nome)
                jogador.treinadores_disponiveis -= 1
                txt_adicional = "+1 Treinador Dominante no Mapa."

        jogador.equipes_baixadas.append(equipe)

        for i in sorted(indices_cartas, reverse=True):
            jogador.mao.pop(i)

        sobras = jogador.descartar_mao()
        self.mercado_aberto.extend(sobras)

        self.add_log(
            f"{jogador.nome} desceu Equipe de "
            f"{equipe.tamanho_da_equipe()} em {regiao.nome}. "
            f"{txt_adicional}"
        )
        self.passar_turno()
        return True, "Transacao Sistemica Comprovada."

    def encerrar_era_e_contar_pv(self):
        self.add_log(
            "=== COMPUTANDO ESPOLIOS E FECHANDO TRILHAS DA ERA ==="
        )
        for j in self.jogadores:
            pts = sum(
                CalculadorDominio.pontos_por_tamanho(
                    eq.tamanho_da_equipe()
                ) for eq in j.equipes_baixadas
            )
            j.pv += pts
            self.add_log(
                f"{j.nome} faturou +{pts}PV pelas equipes."
            )

        for reg in self.mapa_regioes.values():
            ganhos = CalculadorDominio.tabular_fatura_de_regiao(
                reg, self.era_atual, self.jogadores
            )
            for nome, valor in ganhos.items():
                if valor > 0:
                    jogador = next(
                        jn for jn in self.jogadores if jn.nome == nome
                    )
                    jogador.pv += valor
                    self.add_log(
                        f"{nome} arrancou o tesouro de "
                        f"{reg.nome} (+{valor}PV)."
                    )

        self.era_atual += 1
        if self.era_atual > self.max_eras:
            vencedor = sorted(
                self.jogadores, key=lambda x: x.pv, reverse=True
            )[0]
            self.add_log(
                f"\nJOGO ACABOU!\n"
                f"O Campeao do PokEthnos e {vencedor.nome} "
                f"com {vencedor.pv} Pontos!"
            )
        else:
            self.iniciar_nova_era()
