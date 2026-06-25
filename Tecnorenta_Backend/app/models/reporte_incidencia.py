import enum

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class GravedadIncidencia(str, enum.Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"


class EstadoIncidencia(str, enum.Enum):
    ABIERTO = "abierto"
    EN_ATENCION = "en_atencion"
    CERRADO = "cerrado"


class ReporteIncidencia(Base):
    __tablename__ = "reportes_incidencia"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(500), nullable=False)
    gravedad = Column(Enum(GravedadIncidencia), nullable=False)
    url_foto = Column(String(500), nullable=True)
    estado = Column(Enum(EstadoIncidencia), default=EstadoIncidencia.ABIERTO, nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id"), nullable=False)
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    modificado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_modificacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    activo = relationship("Activo", back_populates="reportes")
    mantenimiento_correctivo = relationship("MantenimientoCorrectivo", back_populates="reporte_origen")
