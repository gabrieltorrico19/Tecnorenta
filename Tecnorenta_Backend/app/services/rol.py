from fastapi import HTTPException, status

from app.models.rol import Rol
from app.repositories.rol import RolRepository
from app.schemas.rol import RolCreate, RolUpdate


class RolService:
    def __init__(self, repo: RolRepository):
        self.repo = repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Rol]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, rol_id: int) -> Rol:
        rol = self.repo.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        return rol

    def crear(self, data: RolCreate) -> Rol:
        existente = self.repo.get_by_nombre(data.nombre)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol ya existe")
        rol = Rol(nombre=data.nombre)
        return self.repo.create(rol)

    def actualizar(self, rol_id: int, data: RolUpdate) -> Rol:
        rol = self.obtener(rol_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rol, field, value)
        return self.repo.update(rol)

    def eliminar(self, rol_id: int) -> None:
        rol = self.obtener(rol_id)
        self.repo.delete(rol)
