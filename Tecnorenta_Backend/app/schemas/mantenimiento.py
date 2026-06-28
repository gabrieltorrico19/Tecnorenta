from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.mantenimiento import TipoMantenimiento


class MantenimientoBase(BaseModel):
    tipo: TipoMantenimiento
    fecha: date
    costo: float = 0.0
    descripcion: Optional[str] = None
    url_foto: Optional[str] = None
    id_activo: int
    frecuencia_dias: Optional[int] = None
    proxima_fecha: Optional[date] = None
    id_reporte_origen: Optional[int] = None
    tiempo_reparacion: Optional[int] = None


class MantenimientoCreate(MantenimientoBase):
    pass


class MantenimientoUpdate(BaseModel):
    fecha: Optional[date] = None
    costo: Optional[float] = None
    descripcion: Optional[str] = None
    url_foto: Optional[str] = None
    frecuencia_dias: Optional[int] = None
    proxima_fecha: Optional[date] = None
    tiempo_reparacion: Optional[int] = None


class MantenimientoOut(MantenimientoBase):
    id: int

    model_config = {"from_attributes": True}
