from typing import Optional

from sqlalchemy.orm import Session

from app.models.asignacion_activo import AsignacionActivo


class AsignacionActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AsignacionActivo]:
        return self.db.query(AsignacionActivo).offset(skip).limit(limit).all()

    def get_by_id(self, asignacion_id: int) -> Optional[AsignacionActivo]:
        return self.db.query(AsignacionActivo).filter(AsignacionActivo.id == asignacion_id).first()

    def get_by_contrato(self, id_contrato: int) -> list[AsignacionActivo]:
        return self.db.query(AsignacionActivo).filter(AsignacionActivo.id_contrato == id_contrato).all()

    def get_by_activo(self, id_activo: int) -> list[AsignacionActivo]:
        return self.db.query(AsignacionActivo).filter(AsignacionActivo.id_activo == id_activo).all()

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
