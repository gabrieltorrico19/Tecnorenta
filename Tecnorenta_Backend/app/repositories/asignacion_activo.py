from sqlalchemy.orm import Session

from app.models.asignacion_activo import AsignacionActivo


class AsignacionActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AsignacionActivo]:
        return self.db.query(AsignacionActivo).all()

    def get_by_id(self, asignacion_id: int) -> AsignacionActivo | None:
        return self.db.query(AsignacionActivo).filter(AsignacionActivo.id == asignacion_id).first()

    def create(self, asignacion: AsignacionActivo) -> AsignacionActivo:
        self.db.add(asignacion)
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion

    def update(self, asignacion: AsignacionActivo) -> AsignacionActivo:
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion

    def delete(self, asignacion: AsignacionActivo) -> None:
        self.db.delete(asignacion)
        self.db.commit()
