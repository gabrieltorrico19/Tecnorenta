from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard import DashboardService
from app.schemas.dashboard import (
    DashboardStats,
    KpisResponse,
    Recomendacion,
    TendenciasResponse,
    ActivoReporte,
    ContratoProximoVencer,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db)):
    return DashboardService(db).get_stats()


@router.get("/kpis", response_model=KpisResponse)
def kpis(db: Session = Depends(get_db)):
    return DashboardService(db).get_kpis()


@router.get("/recomendaciones", response_model=list[Recomendacion])
def recomendaciones(db: Session = Depends(get_db)):
    return DashboardService(db).get_recomendaciones()


@router.get("/tendencias", response_model=TendenciasResponse)
def tendencias(meses: int = Query(6, ge=2, le=24), db: Session = Depends(get_db)):
    return DashboardService(db).get_tendencias(meses)


@router.get("/activos-reporte", response_model=list[ActivoReporte])
def activos_reporte(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return DashboardService(db).get_activos_reporte(limit)


@router.get("/contratos-proximos-vencer", response_model=list[ContratoProximoVencer])
def contratos_proximos_vencer(dias: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    return DashboardService(db).get_contratos_proximos_vencer(dias)
