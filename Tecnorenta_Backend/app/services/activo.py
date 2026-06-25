from fastapi import HTTPException, status

from app.models.activo import Activo
from app.repositories.activo import ActivoRepository
from app.schemas.activo import ActivoCreate, ActivoUpdate


class ActivoService:
    def __init__(self, repo: ActivoRepository):
        self.repo = repo

    def listar(self) -> list[Activo]:
        return self.repo.get_all()

    def obtener(self, activo_id: int) -> Activo:
        activo = self.repo.get_by_id(activo_id)
        if not activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
        return activo

    def crear(self, data: ActivoCreate) -> Activo:
        existente = self.repo.get_by_codigo(data.codigo_inventario)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de inventario ya existe")
        return self.repo.create(Activo(**data.model_dump()))

    def actualizar(self, activo_id: int, data: ActivoUpdate) -> Activo:
        activo = self.obtener(activo_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(activo, field, value)
        return self.repo.update(activo)

    def eliminar(self, activo_id: int) -> None:
        activo = self.obtener(activo_id)
        self.repo.delete(activo)
