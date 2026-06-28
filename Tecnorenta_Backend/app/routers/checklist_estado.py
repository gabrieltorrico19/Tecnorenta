from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.checklist_estado import ChecklistEstadoRepository
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.services.checklist_estado import ChecklistEstadoService
from app.schemas.checklist_estado import ChecklistEstadoCreate, ChecklistEstadoUpdate, ChecklistEstadoOut

router = APIRouter(prefix="/checklists", tags=["Checklists de Estado"])


def get_service(db: Session = Depends(get_db)) -> ChecklistEstadoService:
    return ChecklistEstadoService(ChecklistEstadoRepository(db), AsignacionActivoRepository(db))


@router.get("/", response_model=list[ChecklistEstadoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{checklist_id}", response_model=ChecklistEstadoOut)
def obtener(checklist_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(checklist_id)


@router.get("/asignacion/{id_asignacion}", response_model=list[ChecklistEstadoOut])
def listar_por_asignacion(id_asignacion: int, db: Session = Depends(get_db)):
    return get_service(db).listar_por_asignacion(id_asignacion)


@router.post("/", response_model=ChecklistEstadoOut, status_code=201)
def crear(data: ChecklistEstadoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{checklist_id}", response_model=ChecklistEstadoOut)
def actualizar(checklist_id: int, data: ChecklistEstadoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(checklist_id, data)


@router.delete("/{checklist_id}", status_code=204)
def eliminar(checklist_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(checklist_id)
