from sqlalchemy.orm import Session

from app.models.reporte_incidencia import ReporteIncidencia


class ReporteIncidenciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ReporteIncidencia]:
        return self.db.query(ReporteIncidencia).all()

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
        self.db.delete(reporte)
        self.db.commit()
