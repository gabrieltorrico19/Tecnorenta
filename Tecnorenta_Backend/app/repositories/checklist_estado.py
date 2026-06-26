from sqlalchemy.orm import Session

from app.models.checklist_estado import ChecklistEstado


class ChecklistEstadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_asignacion(self, asignacion_id: int) -> list[ChecklistEstado]:
        return self.db.query(ChecklistEstado).filter(ChecklistEstado.id_asignacion == asignacion_id).all()

    def get_by_id(self, checklist_id: int) -> ChecklistEstado | None:
        return self.db.query(ChecklistEstado).filter(ChecklistEstado.id == checklist_id).first()

    def create(self, checklist: ChecklistEstado) -> ChecklistEstado:
        self.db.add(checklist)
        self.db.commit()
        self.db.refresh(checklist)
        return checklist

    def update(self, checklist: ChecklistEstado) -> ChecklistEstado:
        self.db.commit()
        self.db.refresh(checklist)
        return checklist

    def delete(self, checklist: ChecklistEstado) -> None:
        self.db.delete(checklist)
        self.db.commit()
