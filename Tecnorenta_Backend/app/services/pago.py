from fastapi import HTTPException, status

from app.models.pago import Pago
from app.repositories.pago import PagoRepository
from app.schemas.pago import PagoCreate, PagoUpdate


class PagoService:
    def __init__(self, repo: PagoRepository):
        self.repo = repo

    def listar(self, skip: int, limit: int, **filtros) -> tuple[list[Pago], int]:
        return self.repo.get_paginated(skip, limit, **filtros)

    def listar_por_contrato(self, contrato_id: int) -> list[Pago]:
        return self.repo.get_by_contrato(contrato_id)

    def obtener(self, pago_id: int) -> Pago:
        pago = self.repo.get_by_id(pago_id)
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        if pago.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        return pago

    def crear(self, data: PagoCreate) -> Pago:
        return self.repo.create(Pago(**data.model_dump()))

    def actualizar(self, pago_id: int, data: PagoUpdate) -> Pago:
        pago = self.obtener(pago_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(pago, field, value)
        return self.repo.update(pago)

    def restaurar(self, pago_id: int) -> Pago:
        pago = self.repo.get_by_id(pago_id)
        if not pago or not pago.fecha_baja:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado o no está eliminado")
        pago.fecha_baja = None
        return self.repo.update(pago)

    def eliminar(self, pago_id: int) -> None:
        pago = self.obtener(pago_id)
        self.repo.delete(pago)
