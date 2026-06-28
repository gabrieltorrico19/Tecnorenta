from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.models.reporte_incidencia import GravedadIncidencia, EstadoIncidencia


class ReporteIncidenciaBase(BaseModel):
    fecha: date
    descripcion: str
    gravedad: GravedadIncidencia
    url_foto: Optional[str] = None
    estado: EstadoIncidencia = EstadoIncidencia.ABIERTO
    id_activo: int


class ReporteIncidenciaCreate(ReporteIncidenciaBase):
    creado_por: Optional[int] = None


class ReporteIncidenciaUpdate(BaseModel):
    descripcion: Optional[str] = None
    gravedad: Optional[GravedadIncidencia] = None
    url_foto: Optional[str] = None
    estado: Optional[EstadoIncidencia] = None
    modificado_por: Optional[int] = None


class ReporteIncidenciaOut(ReporteIncidenciaBase):
    id: int
    creado_por: Optional[int] = None
    modificado_por: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = {"from_attributes": True}
