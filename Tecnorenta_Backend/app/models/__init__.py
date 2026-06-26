from app.models.base import Base
from app.models.rol import Rol, Permiso, rol_permiso
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.contrato import Contrato, EstadoContrato
from app.models.pago import Pago, EstadoPago
from app.models.categoria_activo import CategoriaActivo
from app.models.activo import Activo, EstadoActivo
from app.models.asignacion_activo import AsignacionActivo
from app.models.historial_ubicacion import HistorialUbicacion
from app.models.checklist_estado import ChecklistEstado, MomentoChecklist, EstadoComponente
from app.models.reporte_incidencia import ReporteIncidencia, GravedadIncidencia, EstadoIncidencia
from app.models.mantenimiento import (
    Mantenimiento,
    MantenimientoPreventivo,
    MantenimientoCorrectivo,
    TipoMantenimiento,
)
from app.models.activo_foto import ActivoFoto
