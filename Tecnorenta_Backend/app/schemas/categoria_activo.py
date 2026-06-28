from typing import Optional

from pydantic import BaseModel


class CategoriaActivoBase(BaseModel):
    nombre: str
    nivel: Optional[str] = None
    descripcion: Optional[str] = None
    id_categoria_padre: Optional[int] = None


class CategoriaActivoCreate(CategoriaActivoBase):
    pass


class CategoriaActivoUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel: Optional[str] = None
    descripcion: Optional[str] = None
    id_categoria_padre: Optional[int] = None


class CategoriaActivoOut(CategoriaActivoBase):
    id: int

    model_config = {"from_attributes": True}
