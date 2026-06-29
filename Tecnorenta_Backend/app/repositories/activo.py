from typing import Optional

from sqlalchemy.orm import Session

from app.models.activo import Activo, EstadoActivo


class ActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Activo]:
        return self.db.query(Activo).filter(Activo.estado != EstadoActivo.BAJA).offset(skip).limit(limit).all()

    def get_by_id(self, activo_id: int) -> Optional[Activo]:
        return self.db.query(Activo).filter(Activo.id == activo_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Activo]:
        return self.db.query(Activo).filter(Activo.codigo_inventario == codigo).first()

    def get_by_serie(self, numero_serie: str) -> Optional[Activo]:
        return self.db.query(Activo).filter(Activo.numero_serie == numero_serie).first()

    def create(self, activo: Activo) -> Activo:
        self.db.add(activo)
        self.db.commit()
        self.db.refresh(activo)
        return activo

    def update(self, activo: Activo) -> Activo:
        self.db.commit()
        self.db.refresh(activo)
        return activo

    def soft_delete(self, activo: Activo) -> Activo:
        activo.estado = EstadoActivo.BAJA
        self.db.commit()
        self.db.refresh(activo)
        return activo
