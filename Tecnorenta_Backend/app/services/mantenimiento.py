from fastapi import HTTPException, status

from app.models.mantenimiento import Mantenimiento
from app.repositories.mantenimiento import MantenimientoRepository
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


class MantenimientoService:
    def __init__(self, repo: MantenimientoRepository):
        self.repo = repo

    def listar(self) -> list[Mantenimiento]:
        return self.repo.get_all()

    def listar_por_activo(self, activo_id: int) -> list[Mantenimiento]:
        return self.repo.get_by_activo(activo_id)

    def obtener(self, mantenimiento_id: int) -> Mantenimiento:
        m = self.repo.get_by_id(mantenimiento_id)
        if not m:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
        return m

    def crear(self, data: MantenimientoCreate) -> Mantenimiento:
        return self.repo.create(Mantenimiento(**data.model_dump()))

    def actualizar(self, mantenimiento_id: int, data: MantenimientoUpdate) -> Mantenimiento:
        m = self.obtener(mantenimiento_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(m, field, value)
        return self.repo.update(m)

    def eliminar(self, mantenimiento_id: int) -> None:
        m = self.obtener(mantenimiento_id)
        self.repo.delete(m)
