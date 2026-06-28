from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class AsignacionActivoBase(BaseModel):
    fecha_asignacion: date
    fecha_devolucion: Optional[date] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    id_contrato: int
    id_activo: int


class AsignacionActivoCreate(AsignacionActivoBase):
    creado_por: Optional[int] = None


class AsignacionActivoUpdate(BaseModel):
    fecha_devolucion: Optional[date] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    modificado_por: Optional[int] = None


class AsignacionActivoOut(AsignacionActivoBase):
    id: int
    creado_por: Optional[int] = None
    modificado_por: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = {"from_attributes": True}
