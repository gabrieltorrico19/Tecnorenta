from typing import Optional

from sqlalchemy.orm import Session

from app.models.checklist_estado import ChecklistEstado


class ChecklistEstadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ChecklistEstado]:
        return self.db.query(ChecklistEstado).offset(skip).limit(limit).all()

    def get_by_id(self, checklist_id: int) -> Optional[ChecklistEstado]:
        return self.db.query(ChecklistEstado).filter(ChecklistEstado.id == checklist_id).first()

    def get_by_asignacion(self, id_asignacion: int) -> list[ChecklistEstado]:
        return self.db.query(ChecklistEstado).filter(ChecklistEstado.id_asignacion == id_asignacion).all()

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
