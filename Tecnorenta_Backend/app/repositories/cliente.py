from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Cliente]:
        return self.db.query(Cliente).all()

    def get_paginated(
        self,
        skip: int,
        limit: int,
        q: str | None = None,
        sector: str | None = None,
    ) -> tuple[list[Cliente], int]:
        query = self.db.query(Cliente)
        if q:
            like = f"%{q}%"
            query = query.filter(or_(
                Cliente.razon_social.ilike(like),
                Cliente.nit.ilike(like),
            ))
        if sector:
            query = query.filter(Cliente.sector == sector)
        total = query.count()
        items = query.order_by(Cliente.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_nit(self, nit: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.nit == nit).first()

    def create(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def update(self, cliente: Cliente) -> Cliente:
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()
