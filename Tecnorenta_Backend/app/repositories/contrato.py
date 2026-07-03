from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.contrato import Contrato, EstadoContrato


class ContratoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Contrato]:
        return self.db.query(Contrato).filter(Contrato.fecha_baja.is_(None)).all()

    def get_paginated(
        self,
        skip: int,
        limit: int,
        estado: EstadoContrato | None = None,
        id_cliente: int | None = None,
    ) -> tuple[list[Contrato], int]:
        query = self.db.query(Contrato).filter(Contrato.fecha_baja.is_(None))
        if estado is not None:
            query = query.filter(Contrato.estado == estado)
        if id_cliente is not None:
            query = query.filter(Contrato.id_cliente == id_cliente)
        total = query.count()
        items = query.order_by(Contrato.id.desc()).offset(skip).limit(limit).all()
        return items, total

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
        contrato.fecha_baja = datetime.now(timezone.utc)
        self.db.commit()
