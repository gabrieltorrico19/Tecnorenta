from fastapi import HTTPException, status

from app.models.reporte_incidencia import ReporteIncidencia
from app.repositories.reporte_incidencia import ReporteIncidenciaRepository
from app.repositories.activo import ActivoRepository
from app.schemas.reporte_incidencia import ReporteIncidenciaCreate, ReporteIncidenciaUpdate


class ReporteIncidenciaService:
    def __init__(self, repo: ReporteIncidenciaRepository, activo_repo: ActivoRepository):
        self.repo = repo
        self.activo_repo = activo_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[ReporteIncidencia]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, reporte_id: int) -> ReporteIncidencia:
        reporte = self.repo.get_by_id(reporte_id)
        if not reporte:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte de incidencia no encontrado")
        return reporte

    def listar_por_activo(self, id_activo: int) -> list[ReporteIncidencia]:
        return self.repo.get_by_activo(id_activo)

    def crear(self, data: ReporteIncidenciaCreate) -> ReporteIncidencia:
        activo = self.activo_repo.get_by_id(data.id_activo)
        if not activo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activo no encontrado")
        reporte = ReporteIncidencia(**data.model_dump())
        return self.repo.create(reporte)

    def actualizar(self, reporte_id: int, data: ReporteIncidenciaUpdate) -> ReporteIncidencia:
        reporte = self.obtener(reporte_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(reporte, field, value)
        return self.repo.update(reporte)

    def eliminar(self, reporte_id: int) -> ReporteIncidencia:
        reporte = self.obtener(reporte_id)
        return self.repo.soft_delete(reporte)
