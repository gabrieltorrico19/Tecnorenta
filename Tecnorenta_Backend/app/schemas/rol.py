from pydantic import BaseModel


class RolBase(BaseModel):
    nombre: str


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: str | None = None


class RolOut(RolBase):
    id: int

    model_config = {"from_attributes": True}


class PermisoBase(BaseModel):
    nombre: str
    descripcion: str | None = None


class PermisoCreate(PermisoBase):
    pass


class PermisoOut(PermisoBase):
    id: int

    model_config = {"from_attributes": True}


class RolAsignarPermiso(BaseModel):
    id_permiso: int
