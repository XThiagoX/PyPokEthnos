"""Configuracao de assets e mapeamentos de Pokemon para o motor do jogo."""
import os

# Diretorio raiz do projeto (tres niveis acima: controller/ -> src/ -> projeto/)
RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

# Mapeamento de pasta do tipo no filesystem
TIPO_PASTA = {
    "Planta": "1.planta",
    "Fogo": "15.fogo",
    "Água": "14.agua",
    "Pedra": "6.pedra",
    "Psíquico": "13.psiquico",
    "Lutador": "10.lutador",
}

# Mapeamento completo: {Regiao: {Tipo: (NomePokemon, ArquivoBase)}}
POKEMON_MAPA = {
    "Kanto": {
        "Planta": ("Bulbasaur", "1.bulbasaur"),
        "Fogo": ("Charmander", "4.charmander"),
        "Água": ("Squirtle", "7.squirtle"),
        "Pedra": ("Geodude", "74.geodude"),
        "Psíquico": ("Alakazam", "65.alakazam"),
        "Lutador": ("Machamp", "68.machamp"),
    },
    "Johto": {
        "Planta": ("Chikorita", "152.chikorita"),
        "Fogo": ("Cyndaquil", "155.cyndaquill"),
        "Água": ("Totodile", "158.totodile"),
        "Pedra": ("Sudowoodo", "185.sudowoodo"),
        "Psíquico": ("Espeon", "196.espeon"),
        "Lutador": ("Tyrogue", "236.tyrogue"),
    },
    "Hoenn": {
        "Planta": ("Treecko", "252.treecko"),
        "Fogo": ("Torchic", "255.torchic"),
        "Água": ("Mudkip", "258.mudkip"),
        "Pedra": ("Solrock", "338.solrock"),
        "Psíquico": ("Gardevoir", "282.gardevoir"),
        "Lutador": ("Hariyama", "297.hariyama"),
    },
    "Sinnoh": {
        "Planta": ("Turtwig", "387.turtwig"),
        "Fogo": ("Chimchar", "390.chimchar"),
        "Água": ("Piplup", "393.piplup"),
        "Pedra": ("Cranidos", "408.cranidos"),
        "Psíquico": ("Chingling", "433.chingling"),
        "Lutador": ("Lucario", "448.lucario"),
    },
    "Unova": {
        "Planta": ("Snivy", "495.snivy"),
        "Fogo": ("Tepig", "498.tepig"),
        "Água": ("Oshawott", "501.oshawott"),
        "Pedra": ("Gigalith", "526.gigalith"),
        "Psíquico": ("Musharna", "518.musharna"),
        "Lutador": ("Gurrdurr", "533.gurrdurr"),
    },
    "Kalos": {
        "Planta": ("Chespin", "650.chespin"),
        "Fogo": ("Fennekin", "653.fennekin"),
        "Água": ("Froakie", "656.froakie"),
        "Pedra": ("Barbacle", "689.barbacle"),
        "Psíquico": ("Espurr", "677.espurr"),
        "Lutador": ("Pancham", "674.pancham"),
    },
}

# Imagens das cartas Equipe Rocket
ROCKET_IMAGENS = [
    os.path.join(RAIZ_PROJETO, "assets", "pokemons", "20.rocket",
                 "1.jessie.png"),
    os.path.join(RAIZ_PROJETO, "assets", "pokemons", "20.rocket",
                 "2.meowth.png"),
    os.path.join(RAIZ_PROJETO, "assets", "pokemons", "20.rocket",
                 "3.james.png"),
]

# Imagem do verso da carta (baralho fechado)
CARTA_VERSO_PATH = os.path.join(
    RAIZ_PROJETO, "assets", "pokemons", "Background.png"
)

# Imagens dos mapas das regioes
MAPA_REGIOES_IMAGENS = {
    "Kanto": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Kanto.png"),
    "Johto": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Johto.png"),
    "Hoenn": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Hoenn.png"),
    "Sinnoh": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Sinnoh.png"),
    "Unova": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Unova.png"),
    "Kalos": os.path.join(RAIZ_PROJETO, "assets", "mapas", "Kalos.png"),
}


def resolver_imagem_path(tipo: str, arquivo_base: str) -> str:
    """Constroi o caminho absoluto para a imagem PNG de um Pokemon."""
    pasta = TIPO_PASTA.get(tipo, "")
    if not pasta:
        return ""
    return os.path.join(RAIZ_PROJETO, "assets", "pokemons", pasta,
                        f"{arquivo_base}.png")
