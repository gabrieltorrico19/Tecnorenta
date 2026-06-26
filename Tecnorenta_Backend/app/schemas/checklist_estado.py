from datetime import datetime
from pydantic import BaseModel


class ChecklistEstadoBase(BaseModel):
    id_asignacion: int
    momento: str
    pantalla: str
    teclado: str
    carcasa: str
    cargador: bool
    observaciones: str | None = None
    url_fotos: str | None = None
    id_usuario: int


class ChecklistEstadoCreate(ChecklistEstadoBase):
    pass


class ChecklistEstadoUpdate(BaseModel):
    momento: str | None = None
    pantalla: str | None = None
    teclado: str | None = None
    carcasa: str | None = None
    cargador: bool | None = None
    observaciones: str | None = None
    url_fotos: str | None = None


class ChecklistEstadoOut(ChecklistEstadoBase):
    id: int
    fecha_registro: datetime | None = None

    model_config = {"from_attributes": True}
