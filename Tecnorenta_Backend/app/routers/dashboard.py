from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard import DashboardService
from app.schemas.dashboard import DashboardStats, ContratoProximoVencer

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db)):
    return DashboardService(db).get_stats()


@router.get("/contratos-proximos-vencer", response_model=list[ContratoProximoVencer])
def contratos_proximos_vencer(dias: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    return DashboardService(db).get_contratos_proximos_vencer(dias)
