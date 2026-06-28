from typing import Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Cliente]:
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_nit(self, nit: str) -> Optional[Cliente]:
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
