from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.checklist_estado import ChecklistEstadoRepository
from app.services.checklist_estado import ChecklistEstadoService
from app.schemas.checklist_estado import ChecklistEstadoCreate, ChecklistEstadoUpdate, ChecklistEstadoOut

router = APIRouter(prefix="/checklist", tags=["Checklist de Estado"])


@router.get("/asignacion/{asignacion_id}", response_model=list[ChecklistEstadoOut])
def listar_por_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    return ChecklistEstadoService(ChecklistEstadoRepository(db)).listar_por_asignacion(asignacion_id)


@router.get("/{checklist_id}", response_model=ChecklistEstadoOut)
def obtener(checklist_id: int, db: Session = Depends(get_db)):
    return ChecklistEstadoService(ChecklistEstadoRepository(db)).obtener(checklist_id)


@router.patch("/{checklist_id}", response_model=ChecklistEstadoOut)
def actualizar(checklist_id: int, data: ChecklistEstadoUpdate, db: Session = Depends(get_db)):
    return ChecklistEstadoService(ChecklistEstadoRepository(db)).actualizar(checklist_id, data)


@router.post("/", response_model=ChecklistEstadoOut, status_code=201)
def crear(data: ChecklistEstadoCreate, db: Session = Depends(get_db)):
    return ChecklistEstadoService(ChecklistEstadoRepository(db)).crear(data)


@router.delete("/{checklist_id}", status_code=204)
def eliminar(checklist_id: int, db: Session = Depends(get_db)):
    ChecklistEstadoService(ChecklistEstadoRepository(db)).eliminar(checklist_id)
