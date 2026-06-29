from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.models.activo import EstadoActivo


class ActivoBase(BaseModel):
    codigo_inventario: str
    modelo: str
    numero_serie: str
    estado: EstadoActivo = EstadoActivo.DISPONIBLE
    fecha_compra: Optional[date] = None
    valor_depreciado: float = 0.0
    id_categoria: Optional[int] = None


class ActivoCreate(ActivoBase):
    creado_por: Optional[int] = None


class ActivoUpdate(BaseModel):
    codigo_inventario: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    estado: Optional[EstadoActivo] = None
    fecha_compra: Optional[date] = None
    valor_depreciado: Optional[float] = None
    id_categoria: Optional[int] = None
    modificado_por: Optional[int] = None


class ActivoOut(ActivoBase):
    id: int
    creado_por: Optional[int] = None
    modificado_por: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = {"from_attributes": True}
