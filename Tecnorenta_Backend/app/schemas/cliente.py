from typing import Optional

from pydantic import BaseModel


class ClienteBase(BaseModel):
    razon_social: str
    nit: str
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    sector: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    razon_social: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    sector: Optional[str] = None


class ClienteOut(ClienteBase):
    id: int

    model_config = {"from_attributes": True}
