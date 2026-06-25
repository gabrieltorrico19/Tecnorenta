from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.mantenimiento import MantenimientoRepository
from app.services.mantenimiento import MantenimientoService
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate, MantenimientoOut

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])


@router.get("/", response_model=list[MantenimientoOut])
def listar(db: Session = Depends(get_db)):
    return MantenimientoService(MantenimientoRepository(db)).listar()


@router.get("/activo/{activo_id}", response_model=list[MantenimientoOut])
def listar_por_activo(activo_id: int, db: Session = Depends(get_db)):
    return MantenimientoService(MantenimientoRepository(db)).listar_por_activo(activo_id)


@router.get("/{mantenimiento_id}", response_model=MantenimientoOut)
def obtener(mantenimiento_id: int, db: Session = Depends(get_db)):
    return MantenimientoService(MantenimientoRepository(db)).obtener(mantenimiento_id)


@router.post("/", response_model=MantenimientoOut, status_code=201)
def crear(data: MantenimientoCreate, db: Session = Depends(get_db)):
    return MantenimientoService(MantenimientoRepository(db)).crear(data)


@router.patch("/{mantenimiento_id}", response_model=MantenimientoOut)
def actualizar(mantenimiento_id: int, data: MantenimientoUpdate, db: Session = Depends(get_db)):
    return MantenimientoService(MantenimientoRepository(db)).actualizar(mantenimiento_id, data)


@router.delete("/{mantenimiento_id}", status_code=204)
def eliminar(mantenimiento_id: int, db: Session = Depends(get_db)):
    MantenimientoService(MantenimientoRepository(db)).eliminar(mantenimiento_id)
