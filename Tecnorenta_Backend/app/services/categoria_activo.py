from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categoria_activo import CategoriaActivo
from app.models.activo import Activo
from app.repositories.categoria_activo import CategoriaActivoRepository
from app.schemas.categoria_activo import CategoriaActivoCreate, CategoriaActivoUpdate


class CategoriaActivoService:
    def __init__(self, repo: CategoriaActivoRepository, db: Session | None = None):
        self.repo = repo
        self.db = db

    def listar(self, skip: int, limit: int) -> tuple[list[CategoriaActivo], int]:
        return self.repo.get_paginated(skip, limit)

    def obtener(self, categoria_id: int) -> CategoriaActivo:
        cat = self.repo.get_by_id(categoria_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return cat

    def crear(self, data: CategoriaActivoCreate) -> CategoriaActivo:
        if data.id_categoria_padre:
            padre = self.repo.get_by_id(data.id_categoria_padre)
            if not padre:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoría padre no existe")
        return self.repo.create(CategoriaActivo(**data.model_dump()))

    def actualizar(self, categoria_id: int, data: CategoriaActivoUpdate) -> CategoriaActivo:
        cat = self.obtener(categoria_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cat, field, value)
        return self.repo.update(cat)

    def eliminar(self, categoria_id: int) -> None:
        cat = self.obtener(categoria_id)
        if self.db:
            activos = self.db.query(Activo).filter(Activo.id_categoria == categoria_id).count()
            if activos > 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="No se puede eliminar una categoría con activos asociados")
        self.repo.delete(cat)
