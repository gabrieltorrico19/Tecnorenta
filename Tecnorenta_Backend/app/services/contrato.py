from fastapi import HTTPException, status

from app.models.contrato import Contrato, EstadoContrato
from app.repositories.contrato import ContratoRepository
from app.repositories.cliente import ClienteRepository
from app.schemas.contrato import ContratoCreate, ContratoUpdate


class ContratoService:
    def __init__(self, repo: ContratoRepository, cliente_repo: ClienteRepository):
        self.repo = repo
        self.cliente_repo = cliente_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Contrato]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, contrato_id: int) -> Contrato:
        contrato = self.repo.get_by_id(contrato_id)
        if not contrato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrato no encontrado")
        return contrato

    def listar_por_cliente(self, id_cliente: int) -> list[Contrato]:
        return self.repo.get_by_cliente(id_cliente)

    def crear(self, data: ContratoCreate) -> Contrato:
        cliente = self.cliente_repo.get_by_id(data.id_cliente)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente no encontrado")
        contrato = Contrato(**data.model_dump())
        return self.repo.create(contrato)

    def actualizar(self, contrato_id: int, data: ContratoUpdate) -> Contrato:
        contrato = self.obtener(contrato_id)
        if contrato.estado == EstadoContrato.CANCELADO:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede modificar un contrato cancelado")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contrato, field, value)
        return self.repo.update(contrato)

    def eliminar(self, contrato_id: int) -> Contrato:
        contrato = self.obtener(contrato_id)
        if contrato.estado == EstadoContrato.ACTIVO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cancelar un contrato activo directamente. Cambie su estado primero.",
            )
        return self.repo.soft_delete(contrato)
