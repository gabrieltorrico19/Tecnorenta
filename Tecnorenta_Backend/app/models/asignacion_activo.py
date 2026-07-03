from sqlalchemy import Column, Integer, Date, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class AsignacionActivo(Base):
    __tablename__ = "asignaciones_activo"

    id = Column(Integer, primary_key=True, index=True)
    fecha_asignacion = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    id_contrato = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id"), nullable=False)
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    modificado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_modificacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fecha_baja = Column(DateTime(timezone=True), nullable=True)

    contrato = relationship("Contrato", back_populates="asignaciones")
    activo = relationship("Activo", back_populates="asignaciones")
    historial_ubicacion = relationship("HistorialUbicacion", back_populates="asignacion")
    checklists = relationship("ChecklistEstado", back_populates="asignacion")
