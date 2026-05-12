import random
import math
from models import Carta, Jogador, Regiao, Equipe

class CalculadorDominio:
    """Encarregado exlusivamente por computar vitórias de equipe e rateios por divisão matemática nas regiões"""
    @staticmethod
    def pontos_por_tamanho(tamanho: int) -> int:
        # A escala canônica do manual Ethnos 1a: [1:0, 2:1, 3:3, 4:6, 5:10, 6+:15]
        tabela = {1:0, 2:1, 3:3, 4:6, 5:10}
        return tabela.get(tamanho, 15)
        
    @staticmethod
    def tabular_fatura_de_regiao(regiao: Regiao, era_atual: int, jogadores: list) -> dict:
        """Rateia PV baseado na colocação: 1º / 2º / 3º de acordo com o estágio da Era"""
        if not regiao.fichas_pv: return {}
        # O total de presenças de cada player 
        placar = [(j.nome, regiao.qtd_treinadores(j.nome)) for j in jogadores if regiao.qtd_treinadores(j.nome) > 0]
        if not placar:
            return {}
            
        # Ordena descendente pelo número de peças
        placar.sort(key=lambda x: x[1], reverse=True)
        # Lógica rigorosa englobando empates vai em seguida
        
        ganhos = {j.nome: 0 for j in jogadores}
        # Pela simplicidade do Escopo Enxuto 2 Players (MVP):
        primeiro_colocado = placar[0]
        fichas_ativos = regiao.fichas_pv[:era_atual] 
        # Apenas simulando o ganho bruto do maior valor ao 1st
        # (Futuramente refinaremos divisão matemática 'math.floor')
        ganhos[primeiro_colocado[0]] += max(fichas_ativos) if fichas_ativos else 0
        return ganhos


class ControladorDoJogo:
    def __init__(self):
        self.era_atual = 1
        self.max_eras = 2 # Setup para 2 Players Pass-And-Play
        self.gatilhos_de_fim_de_era = 0
        
        self.jogadores = [Jogador("Ash Ketchum"), Jogador("Gary Oak")]
        self.turno_atual = 0
        
        self.tipos_ativos = ["Planta", "Fogo", "Água", "Pedra", "Psíquico", "Lutador"]
        self.regioes_nomes = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos"]
        
        self.mapa_regioes = {nome: Regiao(nome) for nome in self.regioes_nomes}
        
        # Forjamento Base das fichas aleatórias
        for r in self.mapa_regioes.values():
            r.fichas_pv = sorted([random.randint(1, 3), random.randint(4, 7), random.randint(8, 10)])
            
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
        self.add_log(f"--- INÍCIO DA ERA {self.era_atual} ---")
        self.gatilhos_de_fim_de_era = 0
        self.baralho.clear()
        self.mercado_aberto.clear()
        
        # Limpar mesas e mãos para loop de Era
        for j in self.jogadores:
            j.mao.clear()
            j.equipes_baixadas.clear()
            
        # Povoar baralho puro com a combinatória dos Tipos vs Regiões (12 de cada tipo)
        cartas_base = []
        for t in self.tipos_ativos:
            for r in self.regioes_nomes:
                cartas_base.append(Carta(t, r))
                cartas_base.append(Carta(t, r)) # Dobro de ocorrência para avolumar o baralho
                
        random.shuffle(cartas_base)
        
        # Sacar 1 pra Mão e Abrir Mercado (Dobro de jogadores)
        for j in self.jogadores:
            j.mao.append(cartas_base.pop())
            
        for _ in range(2 * len(self.jogadores)):
            self.mercado_aberto.append(cartas_base.pop())
            
        # Inserção das cartas Equipe Rocket somente na metade derradeira do deck (Gatilho Suspensório)
        ponto_corte = len(cartas_base) // 2
        metade_fundo = cartas_base[:ponto_corte]
        metade_topo = cartas_base[ponto_corte:]
        
        for _ in range(3):
            metade_fundo.append(Carta("Equipe Rocket", "N/A", eh_gatilho_fim_de_era=True))
            
        random.shuffle(metade_fundo)
        # Pilha reversa: o Topo fica no fim da lista do python pra extrairmos em O(1) com pop()
        self.baralho = metade_fundo + metade_topo 
        
    def comprar_carta_do_baralho(self, jogador: Jogador):
        if len(jogador.mao) >= 10:
            return False, "Sua Mão possui Limite de 10 Cartas, Compra Irregular Mapeada (RF04)."
            
        if not self.baralho:
            return False, "Baralho Mestre esvaziado brutalmente."
            
        carta = self.baralho.pop()
        
        if carta.eh_gatilho_fim_de_era:
            self.gatilhos_de_fim_de_era += 1
            self.add_log(f"UMA CARTA DA EQUIPE ROCKET FOI REVELADA! ({self.gatilhos_de_fim_de_era}/3)")
            if self.gatilhos_de_fim_de_era >= 3:
                self.encerrar_era_e_contar_pv()
                return True, "FIM DE ERA ATIVADO!"
            else:
                return self.comprar_carta_do_baralho(jogador) # Ignora foguetes 1 e 2 e repuxa do baralho
                
        jogador.mao.append(carta)
        self.add_log(f"{jogador.nome} comprou {carta} da Nuvem Fechada.")
        self.passar_turno()
        return True, "Compra consolidada."
        
    def comprar_carta_do_mercado(self, jogador: Jogador, index: int):
        if len(jogador.mao) >= 10:
            return False, "Sua Mão possui Limite de 10 Cartas."
        if index < 0 or index >= len(self.mercado_aberto):
            return False, "Carta Inexistente."
            
        carta = self.mercado_aberto.pop(index)
        jogador.mao.append(carta)
        self.add_log(f"{jogador.nome} pescou do mercado {carta}.")
        self.passar_turno()
        return True, "Operação Comercial realizada."
        
    def jogar_equipe(self, jogador: Jogador, indices_cartas: list[int], index_lider: int):
        cartas = [jogador.mao[i] for i in indices_cartas]
        lider = jogador.mao[index_lider]
        
        equipe = Equipe(cartas, lider)
        if not equipe.validar_mesma_regiao_ou_tipo():
            return False, "Sintaxe da Equipe Recusada! Exige Coesão de Typagem ou Zona Específica."
            
        # Analise Demográfica de Área da Cartilha (RF06)
        regiao = self.mapa_regioes[equipe.get_regiao_lider()]
        
        txt_adicional = ""
        if equipe.tamanho_da_equipe() > regiao.qtd_treinadores(jogador.nome):
            if jogador.treinadores_disponiveis > 0:
                regiao.adicionar_treinador(jogador.nome)
                jogador.treinadores_disponiveis -= 1
                txt_adicional = "+1 Treinador Dominante no Mapa."
                
        # Fixar Bando no Chão
        jogador.equipes_baixadas.append(equipe)
        
        # Eliminação da sobra 
        for i in sorted(indices_cartas, reverse=True):
            jogador.mao.pop(i)
            
        sobras = jogador.descartar_mao()
        self.mercado_aberto.extend(sobras)
        
        self.add_log(f"{jogador.nome} desceu Equipe de {equipe.tamanho_da_equipe()} em {regiao.nome}. {txt_adicional}")
        self.passar_turno()
        return True, "Transação Sistêmica Comprovada."

    def encerrar_era_e_contar_pv(self):
        self.add_log("=== COMPUTANDO ESPÓLIOS E FECHANDO TRILHAS DA ERA ===")
        # Pontos por Agrupamento
        for j in self.jogadores:
            pts = sum(CalculadorDominio.pontos_por_tamanho(eq.tamanho_da_equipe()) for eq in j.equipes_baixadas)
            j.pv += pts
            self.add_log(f"{j.nome} faturou +{pts}PV pela robustez de suas equipes.")
            
        # Ponto Geográfico
        for reg in self.mapa_regioes.values():
            ganhos = CalculadorDominio.tabular_fatura_de_regiao(reg, self.era_atual, self.jogadores)
            for nome, valor in ganhos.items():
                if valor > 0:
                    [jn for jn in self.jogadores if jn.nome == nome][0].pv += valor
                    self.add_log(f"{nome} arrancou o tesouro de {reg.nome} (+{valor}PV).")
                    
        self.era_atual += 1
        if self.era_atual > self.max_eras:
            # Fim do Jogo
            vencedor = sorted(self.jogadores, key=lambda x: x.pv, reverse=True)[0]
            self.add_log(f"\n🏆 JOGO ACABOU! 🏆\nO Campeão do PokEthnos é {vencedor.nome} com monstruosos {vencedor.pv} Pontos!")
        else:
            self.iniciar_nova_era()
