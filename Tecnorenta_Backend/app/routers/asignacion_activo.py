from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.repositories.activo import ActivoRepository
from app.repositories.contrato import ContratoRepository
from app.services.asignacion_activo import AsignacionActivoService
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate, AsignacionActivoOut

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones de Activo"])


def get_service(db: Session = Depends(get_db)) -> AsignacionActivoService:
    return AsignacionActivoService(
        AsignacionActivoRepository(db),
        ActivoRepository(db),
        ContratoRepository(db),
    )


@router.get("/", response_model=list[AsignacionActivoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{asignacion_id}", response_model=AsignacionActivoOut)
def obtener(asignacion_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(asignacion_id)


@router.post("/", response_model=AsignacionActivoOut, status_code=201)
def crear(data: AsignacionActivoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{asignacion_id}", response_model=AsignacionActivoOut)
def actualizar(asignacion_id: int, data: AsignacionActivoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(asignacion_id, data)


@router.delete("/{asignacion_id}", status_code=204)
def eliminar(asignacion_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(asignacion_id)
