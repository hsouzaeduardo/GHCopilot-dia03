from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Resultado(BaseModel, Generic[T]):
    """Envelope padrao de TODA resposta da API. Nenhuma rota devolve o tipo cru."""

    sucesso: bool
    dados: T | None = None
    erro: str | None = None

    @classmethod
    def ok(cls, dados: T) -> "Resultado[T]":
        return cls(sucesso=True, dados=dados, erro=None)

    @classmethod
    def falha(cls, erro: str) -> "Resultado[T]":
        return cls(sucesso=False, dados=None, erro=erro)
