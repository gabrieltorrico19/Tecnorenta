from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.models.contrato import EstadoContrato


class ContratoBase(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    condiciones_uso: Optional[str] = None
    estado: EstadoContrato = EstadoContrato.ACTIVO
    monto_mensual: float
    id_cliente: int


class ContratoCreate(ContratoBase):
    creado_por: Optional[int] = None

    @field_validator("fecha_fin")
    @classmethod
    def fecha_fin_posterior(cls, v, info):
        if "fecha_inicio" in info.data and v <= info.data["fecha_inicio"]:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return v

    @field_validator("monto_mensual")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("monto_mensual debe ser mayor a 0")
        return v


class ContratoUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    condiciones_uso: Optional[str] = None
    estado: Optional[EstadoContrato] = None
    monto_mensual: Optional[float] = None
    modificado_por: Optional[int] = None


class ContratoOut(ContratoBase):
    id: int
    creado_por: Optional[int] = None
    modificado_por: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = {"from_attributes": True}
