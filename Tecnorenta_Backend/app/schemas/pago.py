from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator

from app.models.pago import EstadoPago


class PagoBase(BaseModel):
    id_contrato: int
    concepto: str
    monto: float
    fecha: date
    estado: EstadoPago = EstadoPago.PENDIENTE


class PagoCreate(PagoBase):
    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("monto debe ser mayor a 0")
        return v


class PagoUpdate(BaseModel):
    concepto: Optional[str] = None
    monto: Optional[float] = None
    fecha: Optional[date] = None
    estado: Optional[EstadoPago] = None


class PagoOut(PagoBase):
    id: int

    model_config = {"from_attributes": True}
