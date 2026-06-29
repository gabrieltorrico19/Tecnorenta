from typing import Optional

from sqlalchemy.orm import Session

from app.models.pago import Pago


class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Pago]:
        return self.db.query(Pago).offset(skip).limit(limit).all()

    def get_by_id(self, pago_id: int) -> Optional[Pago]:
        return self.db.query(Pago).filter(Pago.id == pago_id).first()

    def get_by_contrato(self, id_contrato: int) -> list[Pago]:
        return self.db.query(Pago).filter(Pago.id_contrato == id_contrato).all()

    def create(self, pago: Pago) -> Pago:
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def update(self, pago: Pago) -> Pago:
        self.db.commit()
        self.db.refresh(pago)
        return pago

    def delete(self, pago: Pago) -> None:
        self.db.delete(pago)
        self.db.commit()
