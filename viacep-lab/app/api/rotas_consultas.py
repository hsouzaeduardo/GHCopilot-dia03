from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencias import obter_listar_consultas
from app.core.casos_uso.listar_consultas import ListarConsultas
from app.core.comum import Resultado
from app.core.modelos import PaginaConsultas

rotas = APIRouter(tags=["consultas"])


@rotas.get("/consultas", response_model=Resultado[PaginaConsultas])
async def listar_consultas(
    caso: ListarConsultas = Depends(obter_listar_consultas),
    pagina: Annotated[int, Query(ge=1)] = 1,
    tamanho_pagina: Annotated[int, Query(ge=1, le=100)] = 10,
) -> Resultado[PaginaConsultas]:
    resultado = await caso.executar()
    return Resultado[PaginaConsultas].ok(
        PaginaConsultas.criar(
            consultas=resultado.dados or [],
            pagina=pagina,
            tamanho_pagina=tamanho_pagina,
        )
    )
