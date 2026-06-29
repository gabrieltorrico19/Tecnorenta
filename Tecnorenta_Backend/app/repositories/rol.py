from typing import Optional

from sqlalchemy.orm import Session

from app.models.rol import Rol, Permiso


class RolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Rol]:
        return self.db.query(Rol).offset(skip).limit(limit).all()

    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        return self.db.query(Rol).filter(Rol.id == rol_id).first()

    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        return self.db.query(Rol).filter(Rol.nombre == nombre).first()

    def create(self, rol: Rol) -> Rol:
        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def update(self, rol: Rol) -> Rol:
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def delete(self, rol: Rol) -> None:
        self.db.delete(rol)
        self.db.commit()


class PermisoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Permiso]:
        return self.db.query(Permiso).all()

    def get_by_id(self, permiso_id: int) -> Optional[Permiso]:
        return self.db.query(Permiso).filter(Permiso.id == permiso_id).first()
