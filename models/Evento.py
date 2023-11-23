from dataclasses import dataclass

@dataclass
class Evento:
    id: int
    titulo: str
    imagem: str
    descricao: str