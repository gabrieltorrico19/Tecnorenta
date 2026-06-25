from datetime import date
from pydantic import BaseModel


class MantenimientoBase(BaseModel):
    tipo: str
    fecha: date
    costo: float = 0.0
    descripcion: str | None = None
    url_foto: str | None = None
    id_activo: int
    frecuencia_dias: int | None = None
    proxima_fecha: date | None = None
    id_reporte_origen: int | None = None
    tiempo_reparacion: int | None = None


class MantenimientoCreate(MantenimientoBase):
    pass


class MantenimientoUpdate(BaseModel):
    costo: float | None = None
    descripcion: str | None = None
    url_foto: str | None = None
    proxima_fecha: date | None = None
    tiempo_reparacion: int | None = None


class MantenimientoOut(MantenimientoBase):
    id: int

    model_config = {"from_attributes": True}
