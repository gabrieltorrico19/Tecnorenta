from fastapi import HTTPException, status

from app.models.activo import Activo, EstadoActivo
from app.repositories.activo import ActivoRepository
from app.schemas.activo import ActivoCreate, ActivoUpdate


class ActivoService:
    def __init__(self, repo: ActivoRepository):
        self.repo = repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Activo]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, activo_id: int) -> Activo:
        activo = self.repo.get_by_id(activo_id)
        if not activo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
        return activo

    def crear(self, data: ActivoCreate) -> Activo:
        if self.repo.get_by_codigo(data.codigo_inventario):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de inventario ya existe")
        if self.repo.get_by_serie(data.numero_serie):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de serie ya existe")
        activo = Activo(**data.model_dump())
        return self.repo.create(activo)

    def actualizar(self, activo_id: int, data: ActivoUpdate) -> Activo:
        activo = self.obtener(activo_id)
        if activo.estado == EstadoActivo.BAJA:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede modificar un activo dado de baja")
        update_data = data.model_dump(exclude_unset=True)
        if "codigo_inventario" in update_data:
            existente = self.repo.get_by_codigo(update_data["codigo_inventario"])
            if existente and existente.id != activo_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de inventario ya existe")
        if "numero_serie" in update_data:
            existente = self.repo.get_by_serie(update_data["numero_serie"])
            if existente and existente.id != activo_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de serie ya existe")
        for field, value in update_data.items():
            setattr(activo, field, value)
        return self.repo.update(activo)

    def eliminar(self, activo_id: int) -> Activo:
        activo = self.obtener(activo_id)
        if activo.estado == EstadoActivo.RENTADO:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede dar de baja un activo rentado")
        return self.repo.soft_delete(activo)
