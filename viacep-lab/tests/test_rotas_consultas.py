import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_listar_consultas_com_historico_populado_retorna_primeira_pagina_por_padrao():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["sucesso"] is True
    dados = corpo["dados"]
    assert len(dados["itens"]) == 10
    assert dados["pagina_atual"] == 1
    assert dados["tamanho_pagina"] == 10
    assert dados["total_registros"] == 42
    assert dados["total_paginas"] == 5
    assert dados["tem_proxima"] is True
    assert dados["tem_anterior"] is False


@pytest.mark.asyncio
async def test_listar_consultas_retorna_recorte_e_metadados_da_pagina_solicitada():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            primeira_resposta = await cliente.get("/consultas", params={"pagina": 1, "tamanho_pagina": 10})
            resposta = await cliente.get("/consultas", params={"pagina": 2, "tamanho_pagina": 10})

    primeira_pagina = primeira_resposta.json()["dados"]["itens"]
    dados = resposta.json()["dados"]
    assert dados["itens"][0]["id"] != primeira_pagina[0]["id"]
    assert len(dados["itens"]) == 10
    assert dados["pagina_atual"] == 2
    assert dados["tamanho_pagina"] == 10
    assert dados["total_registros"] == 42
    assert dados["total_paginas"] == 5
    assert dados["tem_proxima"] is True
    assert dados["tem_anterior"] is True


@pytest.mark.asyncio
async def test_listar_consultas_pagina_fora_do_intervalo_retorna_itens_vazios():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas", params={"pagina": 6, "tamanho_pagina": 10})

    assert resposta.status_code == 200
    dados = resposta.json()["dados"]
    assert dados["itens"] == []
    assert dados["pagina_atual"] == 6
    assert dados["total_paginas"] == 5
    assert dados["tem_proxima"] is False
    assert dados["tem_anterior"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"pagina": 0},
        {"tamanho_pagina": 0},
        {"tamanho_pagina": 101},
    ],
)
async def test_listar_consultas_rejeita_parametros_de_paginacao_fora_dos_limites(params):
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas", params=params)

    assert resposta.status_code == 422
