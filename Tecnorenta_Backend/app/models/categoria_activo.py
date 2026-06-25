from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class CategoriaActivo(Base):
    __tablename__ = "categorias_activo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nivel = Column(String(50), nullable=True)
    descripcion = Column(String(255), nullable=True)
    id_categoria_padre = Column(Integer, ForeignKey("categorias_activo.id"), nullable=True)

    subcategorias = relationship("CategoriaActivo", backref="categoria_padre", remote_side=[id])
    activos = relationship("Activo", back_populates="categoria")
