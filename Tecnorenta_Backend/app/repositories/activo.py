from sqlalchemy.orm import Session

from app.models.activo import Activo


class ActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Activo]:
        return self.db.query(Activo).all()

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
