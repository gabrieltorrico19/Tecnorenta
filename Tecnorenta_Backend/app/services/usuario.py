from typing import Optional

from fastapi import HTTPException, status

from app.models.usuario import Usuario
from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def listar(self) -> list[Usuario]:
        return self.repo.get_all()

    def obtener(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    def crear(self, data: UsuarioCreate) -> Usuario:
        existente = self.repo.get_by_email(data.email)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")
        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            password_hash=hash_password(data.password),
            telefono=data.telefono,
        )
        return self.repo.create(usuario)

    def actualizar(self, usuario_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.obtener(usuario_id)
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(usuario, field, value)
        return self.repo.update(usuario)

    def eliminar(self, usuario_id: int) -> None:
        usuario = self.obtener(usuario_id)
        self.repo.delete(usuario)
