from sqlalchemy import Column, Integer, String, Float, DateTime, func

from app.models.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String(150), nullable=False)
    nit = Column(String(50), unique=True, nullable=False, index=True)
    direccion = Column(String(255), nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    sector = Column(String(100), nullable=True)
    fecha_baja = Column(DateTime(timezone=True), nullable=True)
