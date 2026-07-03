from fastapi import HTTPException, status

from app.models.mantenimiento import (
    Mantenimiento,
    MantenimientoPreventivo,
    MantenimientoCorrectivo,
    TipoMantenimiento,
)
from app.repositories.mantenimiento import MantenimientoRepository
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


class MantenimientoService:
    def __init__(self, repo: MantenimientoRepository):
        self.repo = repo

    def listar(self, skip: int, limit: int, **filtros) -> tuple[list[Mantenimiento], int]:
        return self.repo.get_paginated(skip, limit, **filtros)

    def listar_por_activo(self, activo_id: int) -> list[Mantenimiento]:
        return self.repo.get_by_activo(activo_id)

    def obtener(self, mantenimiento_id: int) -> Mantenimiento:
        m = self.repo.get_by_id(mantenimiento_id)
        if not m:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
        if m.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
        return m

    def crear(self, data: MantenimientoCreate) -> Mantenimiento:
        # El modelo usa herencia polimórfica sobre `tipo`: se debe instanciar la
        # subclase correcta para que SQLAlchemy fije la identidad y no colisione
        # con la columna discriminadora.
        payload = data.model_dump()
        tipo = payload.pop("tipo", None)
        if tipo == TipoMantenimiento.PREVENTIVO.value:
            return self.repo.create(MantenimientoPreventivo(**payload))
        if tipo == TipoMantenimiento.CORRECTIVO.value:
            return self.repo.create(MantenimientoCorrectivo(**payload))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de mantenimiento inválido: use 'preventivo' o 'correctivo'",
        )

    def actualizar(self, mantenimiento_id: int, data: MantenimientoUpdate) -> Mantenimiento:
        m = self.obtener(mantenimiento_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(m, field, value)
        return self.repo.update(m)

    def restaurar(self, mantenimiento_id: int) -> Mantenimiento:
        m = self.repo.get_by_id(mantenimiento_id)
        if not m or not m.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado o no está eliminado")
        m.fecha_baja = None
        return self.repo.update(m)

    def eliminar(self, mantenimiento_id: int) -> None:
        m = self.obtener(mantenimiento_id)
        self.repo.delete(m)
