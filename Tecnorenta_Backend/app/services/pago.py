from fastapi import HTTPException, status

from app.models.pago import Pago
from app.repositories.pago import PagoRepository
from app.repositories.contrato import ContratoRepository
from app.schemas.pago import PagoCreate, PagoUpdate


class PagoService:
    def __init__(self, repo: PagoRepository, contrato_repo: ContratoRepository):
        self.repo = repo
        self.contrato_repo = contrato_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Pago]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, pago_id: int) -> Pago:
        pago = self.repo.get_by_id(pago_id)
        if not pago:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        return pago

    def listar_por_contrato(self, id_contrato: int) -> list[Pago]:
        return self.repo.get_by_contrato(id_contrato)

    def crear(self, data: PagoCreate) -> Pago:
        contrato = self.contrato_repo.get_by_id(data.id_contrato)
        if not contrato:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contrato no encontrado")
        pago = Pago(**data.model_dump())
        return self.repo.create(pago)

    def actualizar(self, pago_id: int, data: PagoUpdate) -> Pago:
        pago = self.obtener(pago_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(pago, field, value)
        return self.repo.update(pago)

    def eliminar(self, pago_id: int) -> None:
        pago = self.obtener(pago_id)
        self.repo.delete(pago)
