from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.asignacion_activo import AsignacionActivo


class AsignacionActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[AsignacionActivo]:
        return self.db.query(AsignacionActivo).filter(AsignacionActivo.fecha_baja.is_(None)).all()

    def get_paginated(self, skip: int, limit: int) -> tuple[list[AsignacionActivo], int]:
        query = self.db.query(AsignacionActivo).filter(AsignacionActivo.fecha_baja.is_(None))
        total = query.count()
        items = query.order_by(AsignacionActivo.id.desc()).offset(skip).limit(limit).all()
        return items, total

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
        asignacion.fecha_baja = datetime.now(timezone.utc)
        self.db.commit()
