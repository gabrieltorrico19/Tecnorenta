from sqlalchemy.orm import Session

from app.models.mantenimiento import Mantenimiento


class MantenimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Mantenimiento]:
        return self.db.query(Mantenimiento).all()

    def get_paginated(self, skip: int, limit: int) -> tuple[list[Mantenimiento], int]:
        query = self.db.query(Mantenimiento)
        total = query.count()
        items = query.order_by(Mantenimiento.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, mantenimiento_id: int) -> Mantenimiento | None:
        return self.db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()

    def get_by_activo(self, activo_id: int) -> list[Mantenimiento]:
        return self.db.query(Mantenimiento).filter(Mantenimiento.id_activo == activo_id).all()

    def create(self, mantenimiento: Mantenimiento) -> Mantenimiento:
        self.db.add(mantenimiento)
        self.db.commit()
        self.db.refresh(mantenimiento)
        return mantenimiento

    def update(self, mantenimiento: Mantenimiento) -> Mantenimiento:
        self.db.commit()
        self.db.refresh(mantenimiento)
        return mantenimiento

    def delete(self, mantenimiento: Mantenimiento) -> None:
        self.db.delete(mantenimiento)
        self.db.commit()
