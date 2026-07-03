from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.activo_foto import ActivoFoto


class ActivoFotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_activo(self, activo_id: int) -> list[ActivoFoto]:
        return self.db.query(ActivoFoto).filter(ActivoFoto.fecha_baja.is_(None), ActivoFoto.id_activo == activo_id).order_by(ActivoFoto.orden).all()

    def get_by_id(self, foto_id: int) -> ActivoFoto | None:
        return self.db.query(ActivoFoto).filter(ActivoFoto.id == foto_id).first()

    def create(self, foto: ActivoFoto) -> ActivoFoto:
        self.db.add(foto)
        self.db.commit()
        self.db.refresh(foto)
        return foto

    def delete(self, foto: ActivoFoto) -> None:
        foto.fecha_baja = datetime.now(timezone.utc)
        self.db.commit()
