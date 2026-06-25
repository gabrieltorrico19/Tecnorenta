from fastapi import HTTPException, status

from app.models.pago import Pago
from app.repositories.pago import PagoRepository
from app.schemas.pago import PagoCreate


class PagoService:
    def __init__(self, repo: PagoRepository):
        self.repo = repo

    def listar(self) -> list[Pago]:
        return self.repo.get_all()

    def listar_por_contrato(self, contrato_id: int) -> list[Pago]:
        return self.repo.get_by_contrato(contrato_id)

    def obtener(self, pago_id: int) -> Pago:
        pago = self.repo.get_by_id(pago_id)
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        return pago

    def crear(self, data: PagoCreate) -> Pago:
        return self.repo.create(Pago(**data.model_dump()))

    def eliminar(self, pago_id: int) -> None:
        pago = self.obtener(pago_id)
        self.repo.delete(pago)
