from sqlalchemy.orm import Session

from app.models.pago import Pago


class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Pago]:
        return self.db.query(Pago).all()

    def get_by_id(self, pago_id: int) -> Pago | None:
        return self.db.query(Pago).filter(Pago.id == pago_id).first()

    def get_by_contrato(self, contrato_id: int) -> list[Pago]:
        return self.db.query(Pago).filter(Pago.id_contrato == contrato_id).all()

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
