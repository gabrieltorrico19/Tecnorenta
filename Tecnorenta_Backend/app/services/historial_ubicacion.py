from app.models.historial_ubicacion import HistorialUbicacion
from app.repositories.historial_ubicacion import HistorialUbicacionRepository
from app.schemas.historial_ubicacion import HistorialUbicacionCreate


class HistorialUbicacionService:
    def __init__(self, repo: HistorialUbicacionRepository):
        self.repo = repo

    def listar_por_asignacion(self, asignacion_id: int) -> list[HistorialUbicacion]:
        return self.repo.get_by_asignacion(asignacion_id)

    def crear(self, data: HistorialUbicacionCreate) -> HistorialUbicacion:
        return self.repo.create(HistorialUbicacion(**data.model_dump()))
