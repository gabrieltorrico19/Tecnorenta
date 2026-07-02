from sqlalchemy.orm import Session

from app.models.rol import Rol, Permiso, rol_permiso


class RolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Rol]:
        return self.db.query(Rol).all()

    def get_paginated(self, skip: int, limit: int) -> tuple[list[Rol], int]:
        query = self.db.query(Rol)
        total = query.count()
        items = query.order_by(Rol.id.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_id(self, rol_id: int) -> Rol | None:
        return self.db.query(Rol).filter(Rol.id == rol_id).first()

    def get_by_nombre(self, nombre: str) -> Rol | None:
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

    def asignar_permiso(self, rol: Rol, permiso: Permiso) -> None:
        rol.permisos.append(permiso)
        self.db.commit()

    def remover_permiso(self, rol: Rol, permiso: Permiso) -> None:
        rol.permisos.remove(permiso)
        self.db.commit()


class PermisoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Permiso]:
        return self.db.query(Permiso).all()

    def get_by_id(self, permiso_id: int) -> Permiso | None:
        return self.db.query(Permiso).filter(Permiso.id == permiso_id).first()
