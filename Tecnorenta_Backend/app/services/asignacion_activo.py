from fastapi import HTTPException, status

from app.models.asignacion_activo import AsignacionActivo
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate


class AsignacionActivoService:
    def __init__(self, repo: AsignacionActivoRepository):
        self.repo = repo

    def listar(self) -> list[AsignacionActivo]:
        return self.repo.get_all()

    def obtener(self, asignacion_id: int) -> AsignacionActivo:
        asignacion = self.repo.get_by_id(asignacion_id)
        if not asignacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
        return asignacion

    def crear(self, data: AsignacionActivoCreate) -> AsignacionActivo:
        return self.repo.create(AsignacionActivo(**data.model_dump()))

    def actualizar(self, asignacion_id: int, data: AsignacionActivoUpdate) -> AsignacionActivo:
        asignacion = self.obtener(asignacion_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(asignacion, field, value)
        return self.repo.update(asignacion)

    def eliminar(self, asignacion_id: int) -> None:
        asignacion = self.obtener(asignacion_id)
        self.repo.delete(asignacion)
