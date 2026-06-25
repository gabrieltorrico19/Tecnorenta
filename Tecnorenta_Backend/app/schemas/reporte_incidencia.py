from datetime import date, datetime
from pydantic import BaseModel


class ReporteIncidenciaBase(BaseModel):
    fecha: date
    descripcion: str
    gravedad: str
    url_foto: str | None = None
    estado: str = "abierto"
    id_activo: int


class ReporteIncidenciaCreate(ReporteIncidenciaBase):
    pass


class ReporteIncidenciaUpdate(BaseModel):
    descripcion: str | None = None
    gravedad: str | None = None
    url_foto: str | None = None
    estado: str | None = None


class ReporteIncidenciaOut(ReporteIncidenciaBase):
    id: int

    model_config = {"from_attributes": True}
