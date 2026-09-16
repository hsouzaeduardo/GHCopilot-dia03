from app.core.modelos import Consulta


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._consultas: list[Consulta] = []

    async def registrar(self, consulta: Consulta) -> None:
        self._consultas.append(consulta)

    async def listar(self) -> list[Consulta]:
        return sorted(self._consultas, key=lambda item: item.consultado_em, reverse=True)
