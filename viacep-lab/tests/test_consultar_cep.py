import pytest

from app.core.casos_uso.consultar_cep import ConsultarCep
from app.core.modelos import Consulta, Endereco


# Convencao de nome: test_<metodo>_<cenario>_<resultado_esperado>
# Fakes escritos a mao. Este repositorio nao usa unittest.mock nem pytest-mock.
class ProviderFalso:
    def __init__(self, endereco: Endereco | None) -> None:
        self._endereco = endereco

    async def buscar(self, cep: str) -> Endereco | None:
        return self._endereco


class RepositorioFalso:
    def __init__(self) -> None:
        self.registradas: list[Consulta] = []

    async def registrar(self, consulta: Consulta) -> None:
        self.registradas.append(consulta)

    async def listar(self) -> list[Consulta]:
        return self.registradas


PAULISTA = Endereco(
    cep="01310100",
    logradouro="Avenida Paulista",
    bairro="Bela Vista",
    localidade="Sao Paulo",
    uf="SP",
)


@pytest.mark.asyncio
async def test_executar_cep_com_formato_invalido_retorna_falha():
    caso = ConsultarCep(ProviderFalso(None), RepositorioFalso())

    resultado = await caso.executar("123")

    assert resultado.sucesso is False
    assert resultado.erro == "cep-invalido"


@pytest.mark.asyncio
async def test_executar_cep_existente_retorna_endereco():
    caso = ConsultarCep(ProviderFalso(PAULISTA), RepositorioFalso())

    resultado = await caso.executar("01310-100")

    assert resultado.sucesso is True
    assert resultado.dados is not None
    assert resultado.dados.logradouro == "Avenida Paulista"


@pytest.mark.asyncio
async def test_executar_cep_inexistente_registra_consulta_nao_encontrada():
    repositorio = RepositorioFalso()
    caso = ConsultarCep(ProviderFalso(None), repositorio)

    await caso.executar("99999999")

    assert len(repositorio.registradas) == 1
    assert repositorio.registradas[0].encontrado is False
    assert repositorio.registradas[0].cep == "99999999"
