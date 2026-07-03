from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.asignacion_activo import AsignacionActivo
from app.models.activo import Activo, EstadoActivo
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate


class AsignacionActivoService:
    def __init__(self, repo: AsignacionActivoRepository, db: Session | None = None):
        self.repo = repo
        self.db = db

    def listar(self, skip: int, limit: int) -> tuple[list[AsignacionActivo], int]:
        return self.repo.get_paginated(skip, limit)

    def obtener(self, asignacion_id: int) -> AsignacionActivo:
        asignacion = self.repo.get_by_id(asignacion_id)
        if not asignacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
        if asignacion.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
        return asignacion

    def crear(self, data: AsignacionActivoCreate) -> AsignacionActivo:
        if self.db:
            activo = self.db.query(Activo).filter(Activo.id == data.id_activo).first()
            if activo and activo.estado == EstadoActivo.MANTENIMIENTO:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="No se puede asignar un activo que está en mantenimiento")
        return self.repo.create(AsignacionActivo(**data.model_dump()))

    def actualizar(self, asignacion_id: int, data: AsignacionActivoUpdate) -> AsignacionActivo:
        asignacion = self.obtener(asignacion_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(asignacion, field, value)
        return self.repo.update(asignacion)

    def restaurar(self, asignacion_id: int) -> AsignacionActivo:
        asignacion = self.repo.get_by_id(asignacion_id)
        if not asignacion or not asignacion.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada o no está eliminada")
        asignacion.fecha_baja = None
        return self.repo.update(asignacion)

    def eliminar(self, asignacion_id: int) -> None:
        asignacion = self.obtener(asignacion_id)
        self.repo.delete(asignacion)
