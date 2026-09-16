import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_listar_consultas_com_historico_populado_retorna_envelope():
    transporte = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transporte, base_url="http://teste") as cliente:
            resposta = await cliente.get("/consultas")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["sucesso"] is True
    assert len(corpo["dados"]) == 42
