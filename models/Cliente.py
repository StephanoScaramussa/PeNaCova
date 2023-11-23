# models/Aluno.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: int
    nome: str
    cpf : str
    telefone: str
    email: str
    senha: Optional[str] = ""
    token: Optional[str] = ""
    admin: Optional[bool] = False