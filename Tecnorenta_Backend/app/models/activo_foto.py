from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class ActivoFoto(Base):
    __tablename__ = "activos_fotos"

    id = Column(Integer, primary_key=True, index=True)
    id_activo = Column(Integer, ForeignKey("activos.id"), nullable=False)
    url = Column(String(500), nullable=False)
    orden = Column(Integer, default=0)
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now())

    activo = relationship("Activo", back_populates="fotos")
