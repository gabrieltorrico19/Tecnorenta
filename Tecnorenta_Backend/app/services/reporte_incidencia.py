from fastapi import HTTPException, status

from app.models.reporte_incidencia import ReporteIncidencia
from app.repositories.reporte_incidencia import ReporteIncidenciaRepository
from app.schemas.reporte_incidencia import ReporteIncidenciaCreate, ReporteIncidenciaUpdate


class ReporteIncidenciaService:
    def __init__(self, repo: ReporteIncidenciaRepository):
        self.repo = repo

    def listar(self) -> list[ReporteIncidencia]:
        return self.repo.get_all()

    def obtener(self, reporte_id: int) -> ReporteIncidencia:
        reporte = self.repo.get_by_id(reporte_id)
        if not reporte:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")
        return reporte

    def crear(self, data: ReporteIncidenciaCreate) -> ReporteIncidencia:
        return self.repo.create(ReporteIncidencia(**data.model_dump()))

    def actualizar(self, reporte_id: int, data: ReporteIncidenciaUpdate) -> ReporteIncidencia:
        reporte = self.obtener(reporte_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(reporte, field, value)
        return self.repo.update(reporte)

    def eliminar(self, reporte_id: int) -> None:
        reporte = self.obtener(reporte_id)
        self.repo.delete(reporte)
