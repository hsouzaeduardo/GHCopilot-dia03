import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api import rotas_consultas, rotas_enderecos
from app.infra.repositorio_memoria import RepositorioEmMemoria
from app.infra.viacep_http import BASE_URL
from app.seed import popular


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    app.state.repositorio = RepositorioEmMemoria()
    app.state.cliente_http = httpx.AsyncClient(base_url=BASE_URL, timeout=5.0)

    if os.getenv("AMBIENTE", "desenvolvimento") == "desenvolvimento":
        await popular(app.state.repositorio)

    yield

    await app.state.cliente_http.aclose()


app = FastAPI(title="ViaCEP API", version="1.0.0", lifespan=ciclo_de_vida)

app.include_router(rotas_enderecos.rotas)
app.include_router(rotas_consultas.rotas)
