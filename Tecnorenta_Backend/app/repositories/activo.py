from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.activo import Activo, EstadoActivo


class ActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Activo]:
        return self.db.query(Activo).all()

    def get_paginated(
        self,
        skip: int,
        limit: int,
        estado: EstadoActivo | None = None,
        id_categoria: int | None = None,
        q: str | None = None,
    ) -> tuple[list[Activo], int]:
        query = self.db.query(Activo)
        if estado is not None:
            query = query.filter(Activo.estado == estado)
        if id_categoria is not None:
            query = query.filter(Activo.id_categoria == id_categoria)
        if q:
            like = f"%{q}%"
            query = query.filter(or_(
                Activo.codigo_inventario.ilike(like),
                Activo.modelo.ilike(like),
                Activo.numero_serie.ilike(like),
            ))
        total = query.count()
        items = query.order_by(Activo.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, activo_id: int) -> Activo | None:
        return self.db.query(Activo).filter(Activo.id == activo_id).first()

    def get_by_codigo(self, codigo: str) -> Activo | None:
        return self.db.query(Activo).filter(Activo.codigo_inventario == codigo).first()

    def get_by_serie(self, serie: str) -> Activo | None:
        return self.db.query(Activo).filter(Activo.numero_serie == serie).first()

    def create(self, activo: Activo) -> Activo:
        self.db.add(activo)
        self.db.commit()
        self.db.refresh(activo)
        return activo

    def update(self, activo: Activo) -> Activo:
        self.db.commit()
        self.db.refresh(activo)
        return activo

    def delete(self, activo: Activo) -> None:
        self.db.delete(activo)
        self.db.commit()
