from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Endereco(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    localidade: str
    uf: str


class Consulta(BaseModel):
    id: UUID
    cep: str
    consultado_em: datetime
    encontrado: bool
