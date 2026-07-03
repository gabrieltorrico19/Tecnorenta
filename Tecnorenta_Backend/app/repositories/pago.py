from datetime import date

from sqlalchemy.orm import Session

from app.models.pago import Pago, EstadoPago


class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Pago]:
        return self.db.query(Pago).all()

    def get_paginated(
        self,
        skip: int,
        limit: int,
        estado: EstadoPago | None = None,
        id_contrato: int | None = None,
        fecha_desde: date | None = None,
        fecha_hasta: date | None = None,
    ) -> tuple[list[Pago], int]:
        query = self.db.query(Pago)
        if estado is not None:
            query = query.filter(Pago.estado == estado)
        if id_contrato is not None:
            query = query.filter(Pago.id_contrato == id_contrato)
        if fecha_desde is not None:
            query = query.filter(Pago.fecha >= fecha_desde)
        if fecha_hasta is not None:
            query = query.filter(Pago.fecha <= fecha_hasta)
        total = query.count()
        items = query.order_by(Pago.id.desc()).offset(skip).limit(limit).all()
        return items, total

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
