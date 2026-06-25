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


class PagoOut(PagoBase):
    id: int

    model_config = {"from_attributes": True}
