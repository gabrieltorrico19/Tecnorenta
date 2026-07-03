from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.pagination import PaginationParams
from app.models.reporte_incidencia import GravedadIncidencia, EstadoIncidencia
from app.repositories.reporte_incidencia import ReporteIncidenciaRepository
from app.services.reporte_incidencia import ReporteIncidenciaService
from app.schemas.common import Page, paginate
from app.schemas.reporte_incidencia import ReporteIncidenciaCreate, ReporteIncidenciaUpdate, ReporteIncidenciaOut

router = APIRouter(prefix="/reportes", tags=["Reportes de Incidencia"])


@router.get("/", response_model=Page[ReporteIncidenciaOut])
def listar(
    pagination: PaginationParams = Depends(),
    gravedad: GravedadIncidencia | None = Query(None, description="Filtrar por gravedad"),
    estado: EstadoIncidencia | None = Query(None, description="Filtrar por estado"),
    id_activo: int | None = Query(None, description="Filtrar por activo"),
    db: Session = Depends(get_db),
):
    items, total = ReporteIncidenciaService(ReporteIncidenciaRepository(db)).listar(
        pagination.skip, pagination.limit,
        gravedad=gravedad, estado=estado, id_activo=id_activo,
    )
    return paginate(items, total, pagination.page, pagination.page_size)


@router.get("/{reporte_id}", response_model=ReporteIncidenciaOut)
def obtener(reporte_id: int, db: Session = Depends(get_db)):
    return ReporteIncidenciaService(ReporteIncidenciaRepository(db)).obtener(reporte_id)


@router.post("/", response_model=ReporteIncidenciaOut, status_code=201)
def crear(data: ReporteIncidenciaCreate, db: Session = Depends(get_db)):
    return ReporteIncidenciaService(ReporteIncidenciaRepository(db)).crear(data)


@router.patch("/{reporte_id}", response_model=ReporteIncidenciaOut)
def actualizar(reporte_id: int, data: ReporteIncidenciaUpdate, db: Session = Depends(get_db)):
    return ReporteIncidenciaService(ReporteIncidenciaRepository(db)).actualizar(reporte_id, data)


@router.delete("/{reporte_id}", status_code=204)
def eliminar(reporte_id: int, db: Session = Depends(get_db)):
    ReporteIncidenciaService(ReporteIncidenciaRepository(db)).eliminar(reporte_id)
