from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.reporte_incidencia import ReporteIncidencia, GravedadIncidencia, EstadoIncidencia


class ReporteIncidenciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ReporteIncidencia]:
        return self.db.query(ReporteIncidencia).filter(ReporteIncidencia.fecha_baja.is_(None)).all()

    def get_paginated(
        self,
        skip: int,
        limit: int,
        gravedad: GravedadIncidencia | None = None,
        estado: EstadoIncidencia | None = None,
        id_activo: int | None = None,
    ) -> tuple[list[ReporteIncidencia], int]:
        query = self.db.query(ReporteIncidencia).filter(ReporteIncidencia.fecha_baja.is_(None))
        if gravedad is not None:
            query = query.filter(ReporteIncidencia.gravedad == gravedad)
        if estado is not None:
            query = query.filter(ReporteIncidencia.estado == estado)
        if id_activo is not None:
            query = query.filter(ReporteIncidencia.id_activo == id_activo)
        total = query.count()
        items = query.order_by(ReporteIncidencia.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, reporte_id: int) -> ReporteIncidencia | None:
        return self.db.query(ReporteIncidencia).filter(ReporteIncidencia.id == reporte_id).first()

    def create(self, reporte: ReporteIncidencia) -> ReporteIncidencia:
        self.db.add(reporte)
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def update(self, reporte: ReporteIncidencia) -> ReporteIncidencia:
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def delete(self, reporte: ReporteIncidencia) -> None:
        reporte.fecha_baja = datetime.now(timezone.utc)
        self.db.commit()
