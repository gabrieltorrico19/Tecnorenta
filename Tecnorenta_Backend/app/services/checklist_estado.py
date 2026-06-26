from fastapi import HTTPException, status

from app.models.checklist_estado import ChecklistEstado
from app.repositories.checklist_estado import ChecklistEstadoRepository
from app.schemas.checklist_estado import ChecklistEstadoCreate, ChecklistEstadoUpdate


class ChecklistEstadoService:
    def __init__(self, repo: ChecklistEstadoRepository):
        self.repo = repo

    def listar_por_asignacion(self, asignacion_id: int) -> list[ChecklistEstado]:
        return self.repo.get_by_asignacion(asignacion_id)

    def obtener(self, checklist_id: int) -> ChecklistEstado:
        checklist = self.repo.get_by_id(checklist_id)
        if not checklist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist no encontrado")
        return checklist

    def crear(self, data: ChecklistEstadoCreate) -> ChecklistEstado:
        return self.repo.create(ChecklistEstado(**data.model_dump()))

    def actualizar(self, checklist_id: int, data: ChecklistEstadoUpdate) -> ChecklistEstado:
        checklist = self.obtener(checklist_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(checklist, field, value)
        return self.repo.update(checklist)

    def eliminar(self, checklist_id: int) -> None:
        checklist = self.obtener(checklist_id)
        self.repo.delete(checklist)
