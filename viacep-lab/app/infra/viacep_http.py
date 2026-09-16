import httpx

from app.core.modelos import Endereco

BASE_URL = "https://viacep.com.br/ws/"


class ViaCepProvider:
    """Cliente HTTP do ViaCEP. E a unica parte do sistema que conhece o formato deles."""

    def __init__(self, cliente: httpx.AsyncClient) -> None:
        self._cliente = cliente

    async def buscar(self, cep: str) -> Endereco | None:
        resposta = await self._cliente.get(f"{cep}/json/")

        if resposta.status_code in (400, 404):
            return None

        resposta.raise_for_status()
        corpo = resposta.json()

        if _tem_erro(corpo):
            return None

        return Endereco(
            cep=corpo.get("cep") or cep,
            logradouro=corpo.get("logradouro") or "",
            bairro=corpo.get("bairro") or "",
            localidade=corpo.get("localidade") or "",
            uf=corpo.get("uf") or "",
        )


def _tem_erro(corpo: dict) -> bool:
    """O ViaCEP ja devolveu 'erro' como booleano e como string ao longo do tempo."""
    erro = corpo.get("erro")
    if isinstance(erro, bool):
        return erro
    if isinstance(erro, str):
        return erro.lower() == "true"
    return False
