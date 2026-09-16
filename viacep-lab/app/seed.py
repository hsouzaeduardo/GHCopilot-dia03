from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.core.contratos import ConsultaRepositorio
from app.core.modelos import Consulta

CEPS = [
    "01310100", "01001000", "04538133", "20040020", "30130010",
    "40020000", "80010000", "90010150", "60060170", "69005040",
    "50030230", "88010400", "29010000", "64000180", "57020000",
]


async def popular(repositorio: ConsultaRepositorio) -> None:
    """Popula o historico em memoria para a API ter o que listar em desenvolvimento."""
    agora = datetime.now(timezone.utc)

    for indice in range(42):
        await repositorio.registrar(
            Consulta(
                id=uuid4(),
                cep=CEPS[indice % len(CEPS)],
                consultado_em=agora - timedelta(minutes=indice * 7),
                encontrado=indice % 9 != 0,
            )
        )
