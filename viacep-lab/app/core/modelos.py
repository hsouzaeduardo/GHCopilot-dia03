from datetime import datetime
from math import ceil
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


class PaginaConsultas(BaseModel):
    itens: list[Consulta]
    pagina_atual: int
    tamanho_pagina: int
    total_registros: int
    total_paginas: int
    tem_proxima: bool
    tem_anterior: bool

    @classmethod
    def criar(
        cls,
        consultas: list[Consulta],
        pagina: int,
        tamanho_pagina: int,
    ) -> "PaginaConsultas":
        total_registros = len(consultas)
        total_paginas = ceil(total_registros / tamanho_pagina)
        inicio = (pagina - 1) * tamanho_pagina
        fim = inicio + tamanho_pagina

        return cls(
            itens=consultas[inicio:fim],
            pagina_atual=pagina,
            tamanho_pagina=tamanho_pagina,
            total_registros=total_registros,
            total_paginas=total_paginas,
            tem_proxima=pagina < total_paginas,
            tem_anterior=pagina > 1,
        )
