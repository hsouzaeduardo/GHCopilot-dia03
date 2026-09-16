from datetime import datetime, timezone
from uuid import uuid4

from app.core.comum import Resultado
from app.core.contratos import ConsultaRepositorio, EnderecoProvider
from app.core.modelos import Consulta, Endereco


class ConsultarCep:
    def __init__(self, provider: EnderecoProvider, repositorio: ConsultaRepositorio) -> None:
        self._provider = provider
        self._repositorio = repositorio

    async def executar(self, cep: str) -> Resultado[Endereco]:
        normalizado = _normalizar(cep)
        if normalizado is None:
            return Resultado[Endereco].falha("cep-invalido")

        endereco = await self._provider.buscar(normalizado)

        await self._repositorio.registrar(
            Consulta(
                id=uuid4(),
                cep=normalizado,
                consultado_em=datetime.now(timezone.utc),
                encontrado=endereco is not None,
            )
        )

        if endereco is None:
            return Resultado[Endereco].falha("cep-nao-encontrado")

        return Resultado[Endereco].ok(endereco)


def _normalizar(cep: str) -> str | None:
    digitos = "".join(caractere for caractere in cep if caractere.isdigit())
    return digitos if len(digitos) == 8 else None
