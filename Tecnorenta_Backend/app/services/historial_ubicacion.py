from fastapi import HTTPException, status

from app.models.historial_ubicacion import HistorialUbicacion
from app.repositories.historial_ubicacion import HistorialUbicacionRepository
from app.schemas.historial_ubicacion import HistorialUbicacionCreate, HistorialUbicacionUpdate


class HistorialUbicacionService:
    def __init__(self, repo: HistorialUbicacionRepository):
        self.repo = repo

    def listar(self) -> list[HistorialUbicacion]:
        return self.repo.get_all()

    def listar_por_asignacion(self, asignacion_id: int) -> list[HistorialUbicacion]:
        return self.repo.get_by_asignacion(asignacion_id)

    def obtener(self, registro_id: int) -> HistorialUbicacion:
        registro = self.repo.get_by_id(registro_id)
        if not registro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de ubicación no encontrado")
        return registro

    def crear(self, data: HistorialUbicacionCreate) -> HistorialUbicacion:
        return self.repo.create(HistorialUbicacion(**data.model_dump()))

    def actualizar(self, registro_id: int, data: HistorialUbicacionUpdate) -> HistorialUbicacion:
        registro = self.obtener(registro_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(registro, field, value)
        return self.repo.update(registro)

    def eliminar(self, registro_id: int) -> None:
        registro = self.obtener(registro_id)
        self.repo.delete(registro)
