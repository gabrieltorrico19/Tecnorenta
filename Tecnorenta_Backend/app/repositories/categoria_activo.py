from sqlalchemy.orm import Session

from app.models.categoria_activo import CategoriaActivo


class CategoriaActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoriaActivo]:
        return self.db.query(CategoriaActivo).all()

    def get_by_id(self, categoria_id: int) -> CategoriaActivo | None:
        return self.db.query(CategoriaActivo).filter(CategoriaActivo.id == categoria_id).first()

    def create(self, cat: CategoriaActivo) -> CategoriaActivo:
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update(self, cat: CategoriaActivo) -> CategoriaActivo:
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def delete(self, cat: CategoriaActivo) -> None:
        self.db.delete(cat)
        self.db.commit()
