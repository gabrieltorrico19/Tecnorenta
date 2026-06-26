from datetime import datetime
from pydantic import BaseModel


class ActivoFotoOut(BaseModel):
    id: int
    id_activo: int
    url: str
    orden: int
    fecha_subida: datetime | None = None

    model_config = {"from_attributes": True}
