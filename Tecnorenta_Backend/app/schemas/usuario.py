from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True
    id_rol: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    password: Optional[str] = None
    id_rol: Optional[int] = None


class UsuarioOut(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
