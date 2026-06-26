from datetime import date
from pydantic import BaseModel


class ActivoBase(BaseModel):
    codigo_inventario: str
    modelo: str
    numero_serie: str
    estado: str = "disponible"
    fecha_compra: date | None = None
    valor_depreciado: float = 0.0
    id_categoria: int | None = None
    latitud: float | None = None
    longitud: float | None = None


class ActivoCreate(ActivoBase):
    pass


class ActivoUpdate(BaseModel):
    codigo_inventario: str | None = None
    modelo: str | None = None
    numero_serie: str | None = None
    estado: str | None = None
    fecha_compra: date | None = None
    valor_depreciado: float | None = None
    id_categoria: int | None = None
    latitud: float | None = None
    longitud: float | None = None


class ActivoOut(ActivoBase):
    id: int

    model_config = {"from_attributes": True}
