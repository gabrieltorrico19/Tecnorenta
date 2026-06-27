from datetime import date
from pydantic import BaseModel


class ContratoBase(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    condiciones_uso: str | None = None
    estado: str = "activo"
    monto_mensual: float
    id_cliente: int


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    condiciones_uso: str | None = None
    estado: str | None = None
    monto_mensual: float | None = None
    id_cliente: int | None = None
    url_documento: str | None = None


class ContratoOut(ContratoBase):
    id: int
    url_documento: str | None = None

    model_config = {"from_attributes": True}
