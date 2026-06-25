from pydantic import BaseModel


class CategoriaActivoBase(BaseModel):
    nombre: str
    nivel: str | None = None
    descripcion: str | None = None
    id_categoria_padre: int | None = None


class CategoriaActivoCreate(CategoriaActivoBase):
    pass


class CategoriaActivoUpdate(BaseModel):
    nombre: str | None = None
    nivel: str | None = None
    descripcion: str | None = None
    id_categoria_padre: int | None = None


class CategoriaActivoOut(CategoriaActivoBase):
    id: int

    model_config = {"from_attributes": True}
