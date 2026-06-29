from fastapi import HTTPException, status

from app.models.checklist_estado import ChecklistEstado
from app.repositories.checklist_estado import ChecklistEstadoRepository
from app.repositories.asignacion_activo import AsignacionActivoRepository
from app.schemas.checklist_estado import ChecklistEstadoCreate, ChecklistEstadoUpdate


class ChecklistEstadoService:
    def __init__(self, repo: ChecklistEstadoRepository, asignacion_repo: AsignacionActivoRepository):
        self.repo = repo
        self.asignacion_repo = asignacion_repo

    def listar(self, skip: int = 0, limit: int = 100) -> list[ChecklistEstado]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, checklist_id: int) -> ChecklistEstado:
        checklist = self.repo.get_by_id(checklist_id)
        if not checklist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist no encontrado")
        return checklist

    def listar_por_asignacion(self, id_asignacion: int) -> list[ChecklistEstado]:
        return self.repo.get_by_asignacion(id_asignacion)

    def crear(self, data: ChecklistEstadoCreate) -> ChecklistEstado:
        asignacion = self.asignacion_repo.get_by_id(data.id_asignacion)
        if not asignacion:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asignación no encontrada")
        checklist = ChecklistEstado(**data.model_dump())
        return self.repo.create(checklist)

    def actualizar(self, checklist_id: int, data: ChecklistEstadoUpdate) -> ChecklistEstado:
        checklist = self.obtener(checklist_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(checklist, field, value)
        return self.repo.update(checklist)

    def eliminar(self, checklist_id: int) -> None:
        checklist = self.obtener(checklist_id)
        self.repo.delete(checklist)
