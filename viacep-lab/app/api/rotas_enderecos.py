from fastapi import APIRouter, Depends, Response, status

from app.api.dependencias import obter_consultar_cep
from app.core.casos_uso.consultar_cep import ConsultarCep
from app.core.comum import Resultado
from app.core.modelos import Endereco

# Convencao do repositorio: rota nenhuma e declarada no main.py.
# Cada area tem seu APIRouter aqui em app/api/.
rotas = APIRouter(tags=["enderecos"])


@rotas.get("/enderecos/{cep}", response_model=Resultado[Endereco])
async def consultar_endereco(
    cep: str,
    resposta: Response,
    caso: ConsultarCep = Depends(obter_consultar_cep),
) -> Resultado[Endereco]:
    resultado = await caso.executar(cep)

    if not resultado.sucesso:
        resposta.status_code = (
            status.HTTP_400_BAD_REQUEST
            if resultado.erro == "cep-invalido"
            else status.HTTP_404_NOT_FOUND
        )

    return resultado
