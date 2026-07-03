from fastapi import HTTPException, status

from app.models.rol import Rol, Permiso
from app.repositories.rol import RolRepository, PermisoRepository
from app.schemas.rol import RolCreate, RolUpdate


class RolService:
    def __init__(self, repo: RolRepository):
        self.repo = repo

    def listar(self, skip: int, limit: int) -> tuple[list[Rol], int]:
        return self.repo.get_paginated(skip, limit)

    def obtener(self, rol_id: int) -> Rol:
        rol = self.repo.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        if rol.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        return rol

    def crear(self, data: RolCreate) -> Rol:
        existente = self.repo.get_by_nombre(data.nombre)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol ya existe")
        return self.repo.create(Rol(**data.model_dump()))

    def actualizar(self, rol_id: int, data: RolUpdate) -> Rol:
        rol = self.obtener(rol_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rol, field, value)
        return self.repo.update(rol)

    def restaurar(self, rol_id: int) -> Rol:
        rol = self.repo.get_by_id(rol_id)
        if not rol or not rol.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado o no está eliminado")
        rol.fecha_baja = None
        return self.repo.update(rol)

    def eliminar(self, rol_id: int) -> None:
        rol = self.obtener(rol_id)
        self.repo.delete(rol)


class PermisoService:
    def __init__(self, repo_permiso: PermisoRepository, repo_rol: RolRepository):
        self.repo_permiso = repo_permiso
        self.repo_rol = repo_rol

    def listar_permisos(self) -> list[Permiso]:
        return self.repo_permiso.get_all()

    def asignar_permiso(self, rol_id: int, permiso_id: int) -> Rol:
        rol = self.repo_rol.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        permiso = self.repo_permiso.get_by_id(permiso_id)
        if not permiso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permiso no encontrado")
        self.repo_rol.asignar_permiso(rol, permiso)
        return rol

    def remover_permiso(self, rol_id: int, permiso_id: int) -> Rol:
        rol = self.repo_rol.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        permiso = self.repo_permiso.get_by_id(permiso_id)
        if not permiso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permiso no encontrado")
        self.repo_rol.remover_permiso(rol, permiso)
        return rol
