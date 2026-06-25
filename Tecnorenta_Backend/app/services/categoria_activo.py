from fastapi import HTTPException, status

from app.models.categoria_activo import CategoriaActivo
from app.repositories.categoria_activo import CategoriaActivoRepository
from app.schemas.categoria_activo import CategoriaActivoCreate, CategoriaActivoUpdate


class CategoriaActivoService:
    def __init__(self, repo: CategoriaActivoRepository):
        self.repo = repo

    def listar(self) -> list[CategoriaActivo]:
        return self.repo.get_all()

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
        self.repo.delete(cat)
