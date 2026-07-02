from fastapi import HTTPException, status

from app.models.cliente import Cliente
from app.repositories.cliente import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    def listar(self, skip: int, limit: int) -> tuple[list[Cliente], int]:
        return self.repo.get_paginated(skip, limit)

    def obtener(self, cliente_id: int) -> Cliente:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return cliente

    def crear(self, data: ClienteCreate) -> Cliente:
        existente = self.repo.get_by_nit(data.nit)
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El NIT ya está registrado")
        return self.repo.create(Cliente(**data.model_dump()))

    def actualizar(self, cliente_id: int, data: ClienteUpdate) -> Cliente:
        cliente = self.obtener(cliente_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cliente, field, value)
        return self.repo.update(cliente)

    def eliminar(self, cliente_id: int) -> None:
        cliente = self.obtener(cliente_id)
        self.repo.delete(cliente)
