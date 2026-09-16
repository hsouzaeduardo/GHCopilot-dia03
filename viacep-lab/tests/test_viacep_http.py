import httpx
import pytest

from app.infra.viacep_http import BASE_URL, ViaCepProvider


def criar_provider(corpo: dict, status_code: int = 200) -> ViaCepProvider:
    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=corpo)

    cliente = httpx.AsyncClient(transport=httpx.MockTransport(responder), base_url=BASE_URL)
    return ViaCepProvider(cliente)


@pytest.mark.asyncio
async def test_buscar_resposta_valida_mapeia_endereco():
    provider = criar_provider(
        {
            "cep": "01310-100",
            "logradouro": "Avenida Paulista",
            "bairro": "Bela Vista",
            "localidade": "Sao Paulo",
            "uf": "SP",
        }
    )

    endereco = await provider.buscar("01310100")

    assert endereco is not None
    assert endereco.bairro == "Bela Vista"
    assert endereco.uf == "SP"


@pytest.mark.asyncio
async def test_buscar_resposta_com_erro_booleano_retorna_nulo():
    provider = criar_provider({"erro": True})

    assert await provider.buscar("99999999") is None


@pytest.mark.asyncio
async def test_buscar_resposta_com_erro_textual_retorna_nulo():
    provider = criar_provider({"erro": "true"})

    assert await provider.buscar("99999999") is None
