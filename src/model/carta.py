class Carta:
    """Entidade que representa uma carta no jogo PokEthnos"""
    def __init__(self, tipo_pokemon: str, area_regiao: str,
                 nome: str = "", imagem_path: str = "",
                 eh_gatilho_fim_de_era: bool = False):
        self.nome = nome
        self.tipo_pokemon = tipo_pokemon
        self.regiao = area_regiao
        self.imagem_path = imagem_path
        self.eh_gatilho_fim_de_era = eh_gatilho_fim_de_era

    def __repr__(self):
        if self.eh_gatilho_fim_de_era:
            return "[EQUIPE ROCKET - FIM DE ERA]"
        if self.nome:
            return f"[{self.nome} | {self.tipo_pokemon} - {self.regiao}]"
        return f"{self.tipo_pokemon} ({self.regiao})"
