from pydantic import BaseModel


class ClienteBase(BaseModel):
    razon_social: str
    nit: str
    direccion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    sector: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    razon_social: str | None = None
    nit: str | None = None
    direccion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    sector: str | None = None


class ClienteOut(ClienteBase):
    id: int

    model_config = {"from_attributes": True}
