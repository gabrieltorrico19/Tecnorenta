from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.categoria_activo import CategoriaActivo


class CategoriaActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoriaActivo]:
        return self.db.query(CategoriaActivo).filter(CategoriaActivo.fecha_baja.is_(None)).all()

    def get_paginated(self, skip: int, limit: int) -> tuple[list[CategoriaActivo], int]:
        query = self.db.query(CategoriaActivo).filter(CategoriaActivo.fecha_baja.is_(None))
        total = query.count()
        items = query.order_by(CategoriaActivo.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, categoria_id: int) -> CategoriaActivo | None:
        return self.db.query(CategoriaActivo).filter(CategoriaActivo.id == categoria_id).first()

    def create(self, cat: CategoriaActivo) -> CategoriaActivo:
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update(self, cat: CategoriaActivo) -> CategoriaActivo:
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def delete(self, cat: CategoriaActivo) -> None:
        cat.fecha_baja = datetime.now(timezone.utc)
        self.db.commit()
