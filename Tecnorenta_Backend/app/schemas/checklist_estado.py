from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.checklist_estado import MomentoChecklist, EstadoComponente


class ChecklistEstadoBase(BaseModel):
    id_asignacion: int
    momento: MomentoChecklist
    pantalla: EstadoComponente
    teclado: EstadoComponente
    carcasa: EstadoComponente
    cargador: bool
    observaciones: Optional[str] = None
    url_fotos: Optional[str] = None
    id_usuario: int


class ChecklistEstadoCreate(ChecklistEstadoBase):
    pass


class ChecklistEstadoUpdate(BaseModel):
    pantalla: Optional[EstadoComponente] = None
    teclado: Optional[EstadoComponente] = None
    carcasa: Optional[EstadoComponente] = None
    cargador: Optional[bool] = None
    observaciones: Optional[str] = None
    url_fotos: Optional[str] = None


class ChecklistEstadoOut(ChecklistEstadoBase):
    id: int
    fecha_registro: Optional[datetime] = None

    model_config = {"from_attributes": True}
