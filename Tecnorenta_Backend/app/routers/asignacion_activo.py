from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.services.asignacion_activo import AsignacionActivoService
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate, AsignacionActivoOut

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones de Activo"])


@router.get("/", response_model=list[AsignacionActivoOut])
def listar(db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).listar()


@router.get("/{asignacion_id}", response_model=AsignacionActivoOut)
def obtener(asignacion_id: int, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).obtener(asignacion_id)


@router.post("/", response_model=AsignacionActivoOut, status_code=201)
def crear(data: AsignacionActivoCreate, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).crear(data)


@router.patch("/{asignacion_id}", response_model=AsignacionActivoOut)
def actualizar(asignacion_id: int, data: AsignacionActivoUpdate, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).actualizar(asignacion_id, data)


@router.delete("/{asignacion_id}", status_code=204)
def eliminar(asignacion_id: int, db: Session = Depends(get_db)):
    AsignacionActivoService(AsignacionActivoRepository(db)).eliminar(asignacion_id)
