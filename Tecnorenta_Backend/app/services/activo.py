from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activo import Activo
from app.models.asignacion_activo import AsignacionActivo
from app.repositories.activo import ActivoRepository
from app.schemas.activo import ActivoCreate, ActivoUpdate


class ActivoService:
    def __init__(self, repo: ActivoRepository, db: Session | None = None):
        self.repo = repo
        self.db = db

    def listar(self) -> list[Activo]:
        activos = self.repo.get_all()
        for a in activos:
            a.categoria_nombre = a.categoria.nombre if a.categoria else None
        return activos

    def obtener(self, activo_id: int) -> Activo:
        activo = self.repo.get_by_id(activo_id)
        if not activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
        activo.categoria_nombre = activo.categoria.nombre if activo.categoria else None
        return activo

    def crear(self, data: ActivoCreate) -> Activo:
        existente = self.repo.get_by_codigo(data.codigo_inventario)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de inventario ya existe")
        if data.numero_serie:
            existente_serie = self.repo.get_by_serie(data.numero_serie)
            if existente_serie:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de serie ya existe")
        return self.repo.create(Activo(**data.model_dump()))

    def actualizar(self, activo_id: int, data: ActivoUpdate) -> Activo:
        activo = self.obtener(activo_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(activo, field, value)
        return self.repo.update(activo)

    def eliminar(self, activo_id: int) -> None:
        activo = self.obtener(activo_id)
        if self.db:
            asignaciones = self.db.query(AsignacionActivo).filter(
                AsignacionActivo.id_activo == activo_id,
                AsignacionActivo.fecha_devolucion.is_(None),
            ).count()
            if asignaciones > 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="No se puede eliminar un activo con asignaciones activas")
        self.repo.delete(activo)
