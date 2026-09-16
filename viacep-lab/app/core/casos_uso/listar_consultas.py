from app.core.comum import Resultado
from app.core.contratos import ConsultaRepositorio
from app.core.modelos import Consulta


class ListarConsultas:
    def __init__(self, repositorio: ConsultaRepositorio) -> None:
        self._repositorio = repositorio

    async def executar(self) -> Resultado[list[Consulta]]:
        consultas = await self._repositorio.listar()
        return Resultado[list[Consulta]].ok(consultas)
