from fastapi import HTTPException, status

from app.models.categoria_activo import CategoriaActivo
from app.repositories.categoria_activo import CategoriaActivoRepository
from app.schemas.categoria_activo import CategoriaActivoCreate, CategoriaActivoUpdate


class CategoriaActivoService:
    def __init__(self, repo: CategoriaActivoRepository):
        self.repo = repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[CategoriaActivo]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, categoria_id: int) -> CategoriaActivo:
        categoria = self.repo.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return categoria

    def crear(self, data: CategoriaActivoCreate) -> CategoriaActivo:
        if data.id_categoria_padre is not None:
            padre = self.repo.get_by_id(data.id_categoria_padre)
            if not padre:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoría padre no existe")
        categoria = CategoriaActivo(**data.model_dump())
        return self.repo.create(categoria)

    def actualizar(self, categoria_id: int, data: CategoriaActivoUpdate) -> CategoriaActivo:
        categoria = self.obtener(categoria_id)
        update_data = data.model_dump(exclude_unset=True)
        if "id_categoria_padre" in update_data and update_data["id_categoria_padre"] == categoria_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Una categoría no puede ser su propio padre")
        for field, value in update_data.items():
            setattr(categoria, field, value)
        return self.repo.update(categoria)

    def eliminar(self, categoria_id: int) -> None:
        categoria = self.obtener(categoria_id)
        self.repo.delete(categoria)
