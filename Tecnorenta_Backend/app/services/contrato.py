from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.contrato import Contrato
from app.repositories.contrato import ContratoRepository
from app.schemas.contrato import ContratoCreate, ContratoUpdate


class ContratoService:
    def __init__(self, repo: ContratoRepository):
        self.repo = repo

    def listar(self, skip: int, limit: int, **filtros) -> tuple[list[Contrato], int]:
        return self.repo.get_paginated(skip, limit, **filtros)

    def obtener(self, contrato_id: int) -> Contrato:
        contrato = self.repo.get_by_id(contrato_id)
        if not contrato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrato no encontrado")
        return contrato

    def crear(self, data: ContratoCreate) -> Contrato:
        if data.fecha_fin <= data.fecha_inicio:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La fecha de fin debe ser posterior a la fecha de inicio")
        return self.repo.create(Contrato(**data.model_dump()))

    def actualizar(self, contrato_id: int, data: ContratoUpdate) -> Contrato:
        contrato = self.obtener(contrato_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contrato, field, value)
        return self.repo.update(contrato)

    def eliminar(self, contrato_id: int) -> None:
        contrato = self.obtener(contrato_id)
        self.repo.delete(contrato)
