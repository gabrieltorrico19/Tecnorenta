from sqlalchemy.orm import Session

from app.models.historial_ubicacion import HistorialUbicacion


class HistorialUbicacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[HistorialUbicacion]:
        return self.db.query(HistorialUbicacion).all()

    def get_by_id(self, registro_id: int) -> HistorialUbicacion | None:
        return self.db.query(HistorialUbicacion).filter(HistorialUbicacion.id == registro_id).first()

    def get_by_asignacion(self, asignacion_id: int) -> list[HistorialUbicacion]:
        return self.db.query(HistorialUbicacion).filter(HistorialUbicacion.id_asignacion == asignacion_id).all()

    def create(self, registro: HistorialUbicacion) -> HistorialUbicacion:
        self.db.add(registro)
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def update(self, registro: HistorialUbicacion) -> HistorialUbicacion:
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def delete(self, registro: HistorialUbicacion) -> None:
        self.db.delete(registro)
        self.db.commit()
