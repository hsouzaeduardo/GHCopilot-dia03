from fastapi import APIRouter, Depends

from app.api.dependencias import obter_listar_consultas
from app.core.casos_uso.listar_consultas import ListarConsultas
from app.core.comum import Resultado
from app.core.modelos import Consulta

rotas = APIRouter(tags=["consultas"])


# Devolve o historico inteiro, sem recorte. Hoje sao dezenas de registros;
# em producao seriam milhares.
@rotas.get("/consultas", response_model=Resultado[list[Consulta]])
async def listar_consultas(
    caso: ListarConsultas = Depends(obter_listar_consultas),
) -> Resultado[list[Consulta]]:
    return await caso.executar()
