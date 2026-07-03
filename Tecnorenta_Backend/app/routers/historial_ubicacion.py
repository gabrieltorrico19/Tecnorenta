from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.pagination import PaginationParams
from app.repositories.historial_ubicacion import HistorialUbicacionRepository
from app.services.historial_ubicacion import HistorialUbicacionService
from app.schemas.common import Page, paginate
from app.schemas.historial_ubicacion import HistorialUbicacionCreate, HistorialUbicacionUpdate, HistorialUbicacionOut

router = APIRouter(prefix="/historial-ubicacion", tags=["Historial de Ubicación"])


@router.get("/", response_model=Page[HistorialUbicacionOut])
def listar(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    items, total = HistorialUbicacionService(HistorialUbicacionRepository(db)).listar(pagination.skip, pagination.limit)
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/asignacion/{asignacion_id}", response_model=list[HistorialUbicacionOut])
def listar_por_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).listar_por_asignacion(asignacion_id)


@router.get("/{registro_id}", response_model=HistorialUbicacionOut)
def obtener(registro_id: int, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).obtener(registro_id)


@router.post("/", response_model=HistorialUbicacionOut, status_code=201)
def crear(data: HistorialUbicacionCreate, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).crear(data)


@router.patch("/{registro_id}", response_model=HistorialUbicacionOut)
def actualizar(registro_id: int, data: HistorialUbicacionUpdate, db: Session = Depends(get_db)):
    return HistorialUbicacionService(HistorialUbicacionRepository(db)).actualizar(registro_id, data)


@router.delete("/{registro_id}", status_code=204)
def eliminar(registro_id: int, db: Session = Depends(get_db)):
    HistorialUbicacionService(HistorialUbicacionRepository(db)).eliminar(registro_id)


@router.post("/{registro_id}/restaurar")
def restaurar(registro_id: int, db: Session = Depends(get_db)):
    HistorialUbicacionService(HistorialUbicacionRepository(db)).restaurar(registro_id)
    return {"message": "Registro de ubicación restaurado exitosamente"}
