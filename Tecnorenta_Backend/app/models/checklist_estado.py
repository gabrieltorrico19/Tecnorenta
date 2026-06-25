import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class MomentoChecklist(str, enum.Enum):
    ENTREGA = "entrega"
    DEVOLUCION = "devolucion"


class EstadoComponente(str, enum.Enum):
    BIEN = "bien"
    RAYADO = "rayado"
    ROTO = "roto"


class ChecklistEstado(Base):
    __tablename__ = "checklist_estado"

    id = Column(Integer, primary_key=True, index=True)
    id_asignacion = Column(Integer, ForeignKey("asignaciones_activo.id"), nullable=False)
    momento = Column(Enum(MomentoChecklist), nullable=False)
    pantalla = Column(Enum(EstadoComponente), nullable=False)
    teclado = Column(Enum(EstadoComponente), nullable=False)
    carcasa = Column(Enum(EstadoComponente), nullable=False)
    cargador = Column(Boolean, nullable=False)
    observaciones = Column(String(500), nullable=True)
    url_fotos = Column(String(500), nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    asignacion = relationship("AsignacionActivo", back_populates="checklists")
    usuario = relationship("Usuario", backref="checklists")
