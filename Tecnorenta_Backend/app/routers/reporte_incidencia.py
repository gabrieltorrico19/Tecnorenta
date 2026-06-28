from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.reporte_incidencia import ReporteIncidenciaRepository
from app.repositories.activo import ActivoRepository
from app.services.reporte_incidencia import ReporteIncidenciaService
from app.schemas.reporte_incidencia import ReporteIncidenciaCreate, ReporteIncidenciaUpdate, ReporteIncidenciaOut

router = APIRouter(prefix="/incidencias", tags=["Reportes de Incidencia"])


def get_service(db: Session = Depends(get_db)) -> ReporteIncidenciaService:
    return ReporteIncidenciaService(ReporteIncidenciaRepository(db), ActivoRepository(db))


@router.get("/", response_model=list[ReporteIncidenciaOut])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    return get_service(db).listar(skip=skip, limit=limit)


@router.get("/{reporte_id}", response_model=ReporteIncidenciaOut)
def obtener(reporte_id: int, db: Session = Depends(get_db)):
    return get_service(db).obtener(reporte_id)


@router.get("/activo/{id_activo}", response_model=list[ReporteIncidenciaOut])
def listar_por_activo(id_activo: int, db: Session = Depends(get_db)):
    return get_service(db).listar_por_activo(id_activo)


@router.post("/", response_model=ReporteIncidenciaOut, status_code=201)
def crear(data: ReporteIncidenciaCreate, db: Session = Depends(get_db)):
    return get_service(db).crear(data)


@router.put("/{reporte_id}", response_model=ReporteIncidenciaOut)
def actualizar(reporte_id: int, data: ReporteIncidenciaUpdate, db: Session = Depends(get_db)):
    return get_service(db).actualizar(reporte_id, data)


@router.delete("/{reporte_id}", response_model=ReporteIncidenciaOut)
def eliminar(reporte_id: int, db: Session = Depends(get_db)):
    return get_service(db).eliminar(reporte_id)
