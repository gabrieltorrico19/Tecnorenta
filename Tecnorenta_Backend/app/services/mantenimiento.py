from fastapi import HTTPException, status

from app.models.mantenimiento import Mantenimiento, MantenimientoPreventivo, MantenimientoCorrectivo, TipoMantenimiento
from app.models.activo import EstadoActivo
from app.repositories.mantenimiento import MantenimientoRepository
from app.repositories.activo import ActivoRepository
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


class MantenimientoService:
    def __init__(self, repo: MantenimientoRepository, activo_repo: ActivoRepository):
        self.repo = repo
        self.activo_repo = activo_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[Mantenimiento]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, mantenimiento_id: int) -> Mantenimiento:
        mantenimiento = self.repo.get_by_id(mantenimiento_id)
        if not mantenimiento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
        return mantenimiento

    def listar_por_activo(self, id_activo: int) -> list[Mantenimiento]:
        return self.repo.get_by_activo(id_activo)

    def crear(self, data: MantenimientoCreate) -> Mantenimiento:
        activo = self.activo_repo.get_by_id(data.id_activo)
        if not activo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activo no encontrado")

        params = data.model_dump()
        if data.tipo == TipoMantenimiento.PREVENTIVO:
            mantenimiento = MantenimientoPreventivo(**params)
        else:
            if not data.id_reporte_origen:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El mantenimiento correctivo requiere un reporte de incidencia de origen",
                )
            mantenimiento = MantenimientoCorrectivo(**params)

        activo.estado = EstadoActivo.MANTENIMIENTO
        self.activo_repo.update(activo)

        return self.repo.create(mantenimiento)

    def actualizar(self, mantenimiento_id: int, data: MantenimientoUpdate) -> Mantenimiento:
        mantenimiento = self.obtener(mantenimiento_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(mantenimiento, field, value)
        return self.repo.update(mantenimiento)

    def eliminar(self, mantenimiento_id: int) -> None:
        mantenimiento = self.obtener(mantenimiento_id)
        self.repo.delete(mantenimiento)
