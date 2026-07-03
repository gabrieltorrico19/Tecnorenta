from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class HistorialUbicacion(Base):
    __tablename__ = "historial_ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    id_asignacion = Column(Integer, ForeignKey("asignaciones_activo.id"), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    asignacion = relationship("AsignacionActivo", back_populates="historial_ubicacion")
    fecha_baja = Column(DateTime(timezone=True), nullable=True)
