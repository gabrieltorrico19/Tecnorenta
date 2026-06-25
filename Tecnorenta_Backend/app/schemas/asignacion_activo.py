from datetime import date
from pydantic import BaseModel


class AsignacionActivoBase(BaseModel):
    fecha_asignacion: date
    fecha_devolucion: date | None = None
    latitud: float | None = None
    longitud: float | None = None
    id_contrato: int
    id_activo: int


class AsignacionActivoCreate(AsignacionActivoBase):
    pass


class AsignacionActivoUpdate(BaseModel):
    fecha_devolucion: date | None = None
    latitud: float | None = None
    longitud: float | None = None


class AsignacionActivoOut(AsignacionActivoBase):
    id: int

    model_config = {"from_attributes": True}
