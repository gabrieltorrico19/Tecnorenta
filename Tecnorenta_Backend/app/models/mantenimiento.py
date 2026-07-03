import enum

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class TipoMantenimiento(str, enum.Enum):
    PREVENTIVO = "preventivo"
    CORRECTIVO = "correctivo"


class Mantenimiento(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoMantenimiento), nullable=False)
    fecha = Column(Date, nullable=False)
    costo = Column(Float, default=0.0)
    descripcion = Column(String(500), nullable=True)
    url_foto = Column(String(500), nullable=True)
    id_activo = Column(Integer, ForeignKey("activos.id"), nullable=False)

    frecuencia_dias = Column(Integer, nullable=True)
    proxima_fecha = Column(Date, nullable=True)

    id_reporte_origen = Column(Integer, ForeignKey("reportes_incidencia.id"), nullable=True)
    tiempo_reparacion = Column(Integer, nullable=True)

    __mapper_args__ = {"polymorphic_on": tipo, "polymorphic_identity": None}

    activo = relationship("Activo", back_populates="mantenimientos")
    fecha_baja = Column(DateTime(timezone=True), nullable=True)


class MantenimientoPreventivo(Mantenimiento):
    __mapper_args__ = {"polymorphic_identity": TipoMantenimiento.PREVENTIVO}


class MantenimientoCorrectivo(Mantenimiento):
    __mapper_args__ = {"polymorphic_identity": TipoMantenimiento.CORRECTIVO}

    reporte_origen = relationship("ReporteIncidencia", back_populates="mantenimiento_correctivo")
