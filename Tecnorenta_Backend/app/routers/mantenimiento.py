from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.pagination import PaginationParams
from app.models.mantenimiento import TipoMantenimiento
from app.repositories.mantenimiento import MantenimientoRepository
from app.services.mantenimiento import MantenimientoService
from app.schemas.common import Page, paginate
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate, MantenimientoOut

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])


@router.get("/", response_model=Page[MantenimientoOut])
def listar(
    pagination: PaginationParams = Depends(),
    tipo: TipoMantenimiento | None = Query(None, description="Filtrar por tipo"),
    id_activo: int | None = Query(None, description="Filtrar por activo"),
    fecha_desde: date | None = Query(None, description="Fecha desde"),
    fecha_hasta: date | None = Query(None, description="Fecha hasta"),
    db: Session = Depends(get_db),
):
    items, total = MantenimientoService(MantenimientoRepository(db)).listar(
        pagination.skip, pagination.limit,
        tipo=tipo, id_activo=id_activo, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
    )
    return paginate(items, total, pagination.page, pagination.page_size)


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


@router.post("/{mantenimiento_id}/restaurar")
def restaurar(mantenimiento_id: int, db: Session = Depends(get_db)):
    MantenimientoService(MantenimientoRepository(db)).restaurar(mantenimiento_id)
    return {"message": "Mantenimiento restaurado exitosamente"}
