from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.activo import ActivoRepository
from app.services.activo import ActivoService
from app.schemas.activo import ActivoCreate, ActivoUpdate, ActivoOut

router = APIRouter(prefix="/activos", tags=["Activos"])


def get_service(db: Session = Depends(get_db)) -> ActivoService:
    return ActivoService(ActivoRepository(db))


@router.get("/", response_model=list[ActivoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{activo_id}", response_model=ActivoOut)
def obtener(activo_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(activo_id)


@router.post("/", response_model=ActivoOut, status_code=201)
def crear(data: ActivoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{activo_id}", response_model=ActivoOut)
def actualizar(activo_id: int, data: ActivoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(activo_id, data)


@router.delete("/{activo_id}", response_model=ActivoOut)
def eliminar(activo_id: int, db: Session = Depends(get_db)):
    return get_service(db).eliminar(activo_id)
