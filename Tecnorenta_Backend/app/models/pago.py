import enum

from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class EstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    VENCIDO = "vencido"


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    id_contrato = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    concepto = Column(String(200), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE, nullable=False)

    contrato = relationship("Contrato", back_populates="pagos")
    fecha_baja = Column(DateTime(timezone=True), nullable=True)
