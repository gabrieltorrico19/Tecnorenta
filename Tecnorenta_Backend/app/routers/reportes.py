from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.reportes import ReportesService

router = APIRouter(prefix="/reportes", tags=["Reportes Gerenciales"])


def get_service(db: Session = Depends(get_db)) -> ReportesService:
    return ReportesService(db)


@router.get("/activos/top-rentados")
def top_activos_rentados(
    fecha_inicio: date = Query(..., description="Fecha inicio YYYY-MM-DD"),
    fecha_fin: date = Query(..., description="Fecha fin YYYY-MM-DD"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return get_service(db).top_activos_rentados(fecha_inicio, fecha_fin, limit)


@router.get("/activos/bajo-disponibilidad")
def activos_bajo_disponibilidad(
    umbral: int = Query(5, ge=1, description="Unidades disponibles mínimas por modelo"),
    db: Session = Depends(get_db),
):
    return get_service(db).activos_bajo_stock_disponible(umbral)


@router.get("/pagos/resumen-por-estado")
def resumen_pagos(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return get_service(db).resumen_pagos_por_estado(fecha_inicio, fecha_fin)


@router.get("/contratos/proximos-a-vencer")
def contratos_proximos_a_vencer(
    dias: int = Query(30, ge=1, le=365, description="Días de anticipación"),
    db: Session = Depends(get_db),
):
    return get_service(db).contratos_proximos_a_vencer(dias)


@router.get("/incidencias/por-gravedad")
def incidencias_por_gravedad(db: Session = Depends(get_db)):
    return get_service(db).incidencias_por_gravedad()


@router.get("/mantenimientos/costo-por-mes")
def costo_mantenimientos_por_mes(db: Session = Depends(get_db)):
    return get_service(db).costo_mantenimientos_por_mes()
