import enum

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class EstadoActivo(str, enum.Enum):
    DISPONIBLE = "disponible"
    RENTADO = "rentado"
    MANTENIMIENTO = "mantenimiento"
    BAJA = "baja"


class Activo(Base):
    __tablename__ = "activos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_inventario = Column(String(50), unique=True, nullable=False, index=True)
    modelo = Column(String(100), nullable=False)
    numero_serie = Column(String(100), unique=True, nullable=False)
    estado = Column(Enum(EstadoActivo), default=EstadoActivo.DISPONIBLE, nullable=False)
    fecha_compra = Column(Date, nullable=True)
    valor_depreciado = Column(Float, default=0.0)
    id_categoria = Column(Integer, ForeignKey("categorias_activo.id"), nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    modificado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_modificacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fecha_baja = Column(DateTime(timezone=True), nullable=True)

    categoria = relationship("CategoriaActivo", back_populates="activos")
    asignaciones = relationship("AsignacionActivo", back_populates="activo")
    reportes = relationship("ReporteIncidencia", back_populates="activo")
    mantenimientos = relationship("Mantenimiento", back_populates="activo")
    fotos = relationship("ActivoFoto", back_populates="activo", cascade="all, delete-orphan")
