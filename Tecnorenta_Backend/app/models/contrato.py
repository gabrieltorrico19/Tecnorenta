import enum

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class EstadoContrato(str, enum.Enum):
    ACTIVO = "activo"
    VENCIDO = "vencido"
    CANCELADO = "cancelado"
    RENOVADO = "renovado"


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    condiciones_uso = Column(String(500), nullable=True)
    estado = Column(Enum(EstadoContrato), default=EstadoContrato.ACTIVO, nullable=False)
    monto_mensual = Column(Float, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    url_documento = Column(String(500), nullable=True)
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    modificado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_modificacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    cliente = relationship("Cliente", backref="contratos")
    asignaciones = relationship("AsignacionActivo", back_populates="contrato")
    pagos = relationship("Pago", back_populates="contrato")
