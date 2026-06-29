from typing import Optional

from sqlalchemy.orm import Session

from app.models.contrato import Contrato, EstadoContrato


class ContratoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Contrato]:
        return (
            self.db.query(Contrato)
            .filter(Contrato.estado != EstadoContrato.CANCELADO)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, contrato_id: int) -> Optional[Contrato]:
        return self.db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def get_by_cliente(self, id_cliente: int) -> list[Contrato]:
        return self.db.query(Contrato).filter(Contrato.id_cliente == id_cliente).all()

    def create(self, contrato: Contrato) -> Contrato:
        self.db.add(contrato)
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def update(self, contrato: Contrato) -> Contrato:
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def soft_delete(self, contrato: Contrato) -> Contrato:
        contrato.estado = EstadoContrato.CANCELADO
        self.db.commit()
        self.db.refresh(contrato)
        return contrato
