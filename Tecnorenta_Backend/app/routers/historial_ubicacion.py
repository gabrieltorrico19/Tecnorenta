from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.historial_ubicacion import HistorialUbicacionRepository
from app.services.historial_ubicacion import HistorialUbicacionService
from app.schemas.historial_ubicacion import HistorialUbicacionCreate, HistorialUbicacionOut

router = APIRouter(prefix="/historial-ubicacion", tags=["Historial de Ubicación"])


@router.get("/asignacion/{asignacion_id}", response_model=list[HistorialUbicacionOut])
def listar_por_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).listar_por_asignacion(asignacion_id)


@router.post("/", response_model=HistorialUbicacionOut, status_code=201)
def crear(data: HistorialUbicacionCreate, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).crear(data)
