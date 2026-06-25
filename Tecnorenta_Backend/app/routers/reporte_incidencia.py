from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.reporte_incidencia import ReporteIncidenciaRepository
from app.services.reporte_incidencia import ReporteIncidenciaService
from app.schemas.reporte_incidencia import ReporteIncidenciaCreate, ReporteIncidenciaUpdate, ReporteIncidenciaOut

router = APIRouter(prefix="/reportes", tags=["Reportes de Incidencia"])


@router.get("/", response_model=list[ReporteIncidenciaOut])
def listar(db: Session = Depends(get_db)):
    return ReporteIncidenciaService(ReporteIncidenciaRepository(db)).listar()


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
