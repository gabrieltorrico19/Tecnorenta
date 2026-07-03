from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


rol_permiso = Table(
    "roles_permisos",
    Base.metadata,
    Column("id_rol", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("id_permiso", Integer, ForeignKey("permisos.id"), primary_key=True),
)


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    fecha_baja = Column(DateTime(timezone=True), nullable=True)

    permisos = relationship("Permiso", secondary=rol_permiso, back_populates="roles")
    usuarios = relationship("Usuario", back_populates="rol")


class Permiso(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)

    roles = relationship("Rol", secondary=rol_permiso, back_populates="permisos")
