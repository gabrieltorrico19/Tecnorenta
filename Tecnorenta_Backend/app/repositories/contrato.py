from sqlalchemy.orm import Session

from app.models.contrato import Contrato


class ContratoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Contrato]:
        return self.db.query(Contrato).all()

    def get_by_id(self, contrato_id: int) -> Contrato | None:
        return self.db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def create(self, contrato: Contrato) -> Contrato:
        self.db.add(contrato)
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def update(self, contrato: Contrato) -> Contrato:
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def delete(self, contrato: Contrato) -> None:
        self.db.delete(contrato)
        self.db.commit()
