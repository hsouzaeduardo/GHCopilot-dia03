import httpx
from fastapi import Request

from app.core.casos_uso.consultar_cep import ConsultarCep
from app.core.casos_uso.listar_consultas import ListarConsultas
from app.infra.viacep_http import ViaCepProvider


def obter_repositorio(request: Request):
    return request.app.state.repositorio


def obter_cliente_http(request: Request) -> httpx.AsyncClient:
    return request.app.state.cliente_http


def obter_consultar_cep(request: Request) -> ConsultarCep:
    return ConsultarCep(
        provider=ViaCepProvider(obter_cliente_http(request)),
        repositorio=obter_repositorio(request),
    )


def obter_listar_consultas(request: Request) -> ListarConsultas:
    return ListarConsultas(repositorio=obter_repositorio(request))
