from datetime import datetime
from pydantic import BaseModel


class HistorialUbicacionBase(BaseModel):
    id_asignacion: int
    latitud: float
    longitud: float


class HistorialUbicacionCreate(HistorialUbicacionBase):
    pass


class HistorialUbicacionUpdate(BaseModel):
    latitud: float | None = None
    longitud: float | None = None


class HistorialUbicacionOut(HistorialUbicacionBase):
    id: int
    timestamp: datetime | None = None

    model_config = {"from_attributes": True}
