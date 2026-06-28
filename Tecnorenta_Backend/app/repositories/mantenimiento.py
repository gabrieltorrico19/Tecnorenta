from typing import Optional

from sqlalchemy.orm import Session

from app.models.mantenimiento import Mantenimiento


class MantenimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Mantenimiento]:
        return self.db.query(Mantenimiento).offset(skip).limit(limit).all()

    def get_by_id(self, mantenimiento_id: int) -> Optional[Mantenimiento]:
        return self.db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()

    def get_by_activo(self, id_activo: int) -> list[Mantenimiento]:
        return self.db.query(Mantenimiento).filter(Mantenimiento.id_activo == id_activo).all()

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
