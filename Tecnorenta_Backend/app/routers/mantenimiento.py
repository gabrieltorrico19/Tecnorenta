from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.mantenimiento import MantenimientoRepository
from app.repositories.activo import ActivoRepository
from app.services.mantenimiento import MantenimientoService
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate, MantenimientoOut

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])


def get_service(db: Session = Depends(get_db)) -> MantenimientoService:
    return MantenimientoService(MantenimientoRepository(db), ActivoRepository(db))


@router.get("/", response_model=list[MantenimientoOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{mantenimiento_id}", response_model=MantenimientoOut)
def obtener(mantenimiento_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(mantenimiento_id)


@router.get("/activo/{id_activo}", response_model=list[MantenimientoOut])
def listar_por_activo(id_activo: int, db: Session = Depends(get_db)):
    return get_service(db).listar_por_activo(id_activo)


@router.post("/", response_model=MantenimientoOut, status_code=201)
def crear(data: MantenimientoCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{mantenimiento_id}", response_model=MantenimientoOut)
def actualizar(mantenimiento_id: int, data: MantenimientoUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(mantenimiento_id, data)


@router.delete("/{mantenimiento_id}", status_code=204)
def eliminar(mantenimiento_id: int, db: Session = Depends(get_db)):
    get_service(db).eliminar(mantenimiento_id)
