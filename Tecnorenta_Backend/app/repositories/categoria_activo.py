from typing import Optional

from sqlalchemy.orm import Session

from app.models.categoria_activo import CategoriaActivo


class CategoriaActivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CategoriaActivo]:
        return self.db.query(CategoriaActivo).offset(skip).limit(limit).all()

    def get_by_id(self, categoria_id: int) -> Optional[CategoriaActivo]:
        return self.db.query(CategoriaActivo).filter(CategoriaActivo.id == categoria_id).first()

    def create(self, categoria: CategoriaActivo) -> CategoriaActivo:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def update(self, categoria: CategoriaActivo) -> CategoriaActivo:
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, categoria: CategoriaActivo) -> None:
        self.db.delete(categoria)
        self.db.commit()
