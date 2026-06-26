from datetime import date
from pydantic import BaseModel


class PagoBase(BaseModel):
    id_contrato: int
    concepto: str
    monto: float
    fecha: date
    estado: str = "pendiente"


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    concepto: str | None = None
    monto: float | None = None
    fecha: date | None = None
    estado: str | None = None


class PagoOut(PagoBase):
    id: int

    model_config = {"from_attributes": True}
