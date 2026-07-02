from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.pagination import PaginationParams
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.services.asignacion_activo import AsignacionActivoService
from app.schemas.common import Page, paginate
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate, AsignacionActivoOut

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones de Activo"])


@router.get("/", response_model=Page[AsignacionActivoOut])
def listar(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    items, total = AsignacionActivoService(AsignacionActivoRepository(db)).listar(pagination.skip, pagination.limit)
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/{asignacion_id}", response_model=AsignacionActivoOut)
def obtener(asignacion_id: int, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).obtener(asignacion_id)


@router.post("/", response_model=AsignacionActivoOut, status_code=201)
def crear(data: AsignacionActivoCreate, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db), db=db).crear(data)


@router.patch("/{asignacion_id}", response_model=AsignacionActivoOut)
def actualizar(asignacion_id: int, data: AsignacionActivoUpdate, db: Session = Depends(get_db)):
    return AsignacionActivoService(AsignacionActivoRepository(db)).actualizar(asignacion_id, data)


@router.delete("/{asignacion_id}", status_code=204)
def eliminar(asignacion_id: int, db: Session = Depends(get_db)):
    AsignacionActivoService(AsignacionActivoRepository(db)).eliminar(asignacion_id)
