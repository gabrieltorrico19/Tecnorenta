from typing import Optional

from sqlalchemy.orm import Session

from app.models.reporte_incidencia import ReporteIncidencia, EstadoIncidencia


class ReporteIncidenciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ReporteIncidencia]:
        return (
            self.db.query(ReporteIncidencia)
            .filter(ReporteIncidencia.estado != EstadoIncidencia.CERRADO)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, reporte_id: int) -> Optional[ReporteIncidencia]:
        return self.db.query(ReporteIncidencia).filter(ReporteIncidencia.id == reporte_id).first()

    def get_by_activo(self, id_activo: int) -> list[ReporteIncidencia]:
        return self.db.query(ReporteIncidencia).filter(ReporteIncidencia.id_activo == id_activo).all()

    def create(self, reporte: ReporteIncidencia) -> ReporteIncidencia:
        self.db.add(reporte)
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def update(self, reporte: ReporteIncidencia) -> ReporteIncidencia:
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def soft_delete(self, reporte: ReporteIncidencia) -> ReporteIncidencia:
        reporte.estado = EstadoIncidencia.CERRADO
        self.db.commit()
        self.db.refresh(reporte)
        return reporte
