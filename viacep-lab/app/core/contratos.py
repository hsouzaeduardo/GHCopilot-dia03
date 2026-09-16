from typing import Protocol

from app.core.modelos import Consulta, Endereco


class EnderecoProvider(Protocol):
    async def buscar(self, cep: str) -> Endereco | None: ...


class ConsultaRepositorio(Protocol):
    async def registrar(self, consulta: Consulta) -> None: ...

    async def listar(self) -> list[Consulta]: ...
