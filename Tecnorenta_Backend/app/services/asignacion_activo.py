from fastapi import HTTPException, status

from app.models.asignacion_activo import AsignacionActivo
from app.models.activo import EstadoActivo
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.repositories.activo import ActivoRepository
from app.repositories.contrato import ContratoRepository
from app.schemas.asignacion_activo import AsignacionActivoCreate, AsignacionActivoUpdate


class AsignacionActivoService:
    def __init__(
        self,
        repo: AsignacionActivoRepository,
        activo_repo: ActivoRepository,
        contrato_repo: ContratoRepository,
    ):
        self.repo = repo
        self.activo_repo = activo_repo
        self.contrato_repo = contrato_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[AsignacionActivo]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, asignacion_id: int) -> AsignacionActivo:
        asignacion = self.repo.get_by_id(asignacion_id)
        if not asignacion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
        return asignacion

    def crear(self, data: AsignacionActivoCreate) -> AsignacionActivo:
        activo = self.activo_repo.get_by_id(data.id_activo)
        if not activo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activo no encontrado")
        if activo.estado != EstadoActivo.DISPONIBLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El activo no está disponible (estado actual: {activo.estado.value})",
            )
        contrato = self.contrato_repo.get_by_id(data.id_contrato)
        if not contrato:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contrato no encontrado")

        asignacion = AsignacionActivo(**data.model_dump())
        resultado = self.repo.create(asignacion)

        activo.estado = EstadoActivo.RENTADO
        self.activo_repo.update(activo)

        return resultado

    def actualizar(self, asignacion_id: int, data: AsignacionActivoUpdate) -> AsignacionActivo:
        asignacion = self.obtener(asignacion_id)
        update_data = data.model_dump(exclude_unset=True)

        if "fecha_devolucion" in update_data and update_data["fecha_devolucion"] is not None:
            activo = self.activo_repo.get_by_id(asignacion.id_activo)
            if activo:
                activo.estado = EstadoActivo.DISPONIBLE
                self.activo_repo.update(activo)

        for field, value in update_data.items():
            setattr(asignacion, field, value)
        return self.repo.update(asignacion)

    def eliminar(self, asignacion_id: int) -> None:
        asignacion = self.obtener(asignacion_id)
        self.repo.delete(asignacion)
