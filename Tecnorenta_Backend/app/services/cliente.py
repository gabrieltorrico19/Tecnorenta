from fastapi import HTTPException, status

from app.models.cliente import Cliente
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Cliente]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, cliente_id: int) -> Cliente:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return cliente

    def crear(self, data: ClienteCreate) -> Cliente:
        existente = self.repo.get_by_nit(data.nit)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El NIT ya está registrado")
        cliente = Cliente(**data.model_dump())
        return self.repo.create(cliente)

    def actualizar(self, cliente_id: int, data: ClienteUpdate) -> Cliente:
        cliente = self.obtener(cliente_id)
        update_data = data.model_dump(exclude_unset=True)
        if "nit" in update_data:
            existente = self.repo.get_by_nit(update_data["nit"])
            if existente and existente.id != cliente_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El NIT ya está registrado")
        for field, value in update_data.items():
            setattr(cliente, field, value)
        return self.repo.update(cliente)

    def eliminar(self, cliente_id: int) -> None:
        cliente = self.obtener(cliente_id)
        self.repo.delete(cliente)
