from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.activo import Activo, EstadoActivo
from app.models.contrato import Contrato, EstadoContrato
from app.models.mantenimiento import Mantenimiento
from app.models.reporte_incidencia import ReporteIncidencia, EstadoIncidencia
from app.models.pago import Pago
from app.schemas.dashboard import DashboardStats, ContratoProximoVencer


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self) -> DashboardStats:
        usuarios_count = self.db.query(func.count(Usuario.id)).scalar() or 0
        clientes_count = self.db.query(func.count(Cliente.id)).scalar() or 0

        activos = self.db.query(Activo).all()
        activos_por_estado: dict[str, int] = {}
        for a in activos:
            estado = a.estado.value if hasattr(a.estado, "value") else str(a.estado)
            activos_por_estado[estado] = activos_por_estado.get(estado, 0) + 1

        contratos = self.db.query(Contrato).all()
        contratos_por_estado: dict[str, int] = {}
        for c in contratos:
            estado = c.estado.value if hasattr(c.estado, "value") else str(c.estado)
            contratos_por_estado[estado] = contratos_por_estado.get(estado, 0) + 1

        hoy = date.today()
        contratos_proximos = self.db.query(func.count(Contrato.id)).filter(
            Contrato.estado == EstadoContrato.ACTIVO,
            Contrato.fecha_fin <= hoy + timedelta(days=30),
            Contrato.fecha_fin >= hoy,
        ).scalar() or 0

        mantenimientos_pendientes = self.db.query(func.count(Mantenimiento.id)).filter(
            Mantenimiento.fecha >= hoy
        ).scalar() or 0

        incidencias_abiertas = self.db.query(func.count(ReporteIncidencia.id)).filter(
            ReporteIncidencia.estado != EstadoIncidencia.CERRADO
        ).scalar() or 0

        pagos_vencidos = self.db.query(func.count(Pago.id)).filter(
            Pago.estado == "vencido"
        ).scalar() or 0

        total_ingresos = self.db.query(func.coalesce(func.sum(Contrato.monto_mensual), 0)).filter(
            Contrato.estado == EstadoContrato.ACTIVO
        ).scalar() or 0.0

        return DashboardStats(
            usuarios_count=usuarios_count,
            clientes_count=clientes_count,
            activos_count=len(activos),
            activos_por_estado=activos_por_estado,
            contratos_count=len(contratos),
            contratos_por_estado=contratos_por_estado,
            contratos_proximos_vencer=contratos_proximos,
            mantenimientos_pendientes=mantenimientos_pendientes,
            incidencias_abiertas=incidencias_abiertas,
            pagos_vencidos=pagos_vencidos,
            total_ingresos_mensuales=float(total_ingresos),
        )

    def get_contratos_proximos_vencer(self, dias: int = 30) -> list[ContratoProximoVencer]:
        hoy = date.today()
        limite = hoy + timedelta(days=dias)
        contratos = self.db.query(Contrato).filter(
            Contrato.estado == EstadoContrato.ACTIVO,
            Contrato.fecha_fin <= limite,
        ).all()

        result = []
        for c in contratos:
            dias_restantes = (c.fecha_fin - hoy).days
            cliente_nombre = c.cliente.razon_social if c.cliente else "—"
            result.append(ContratoProximoVencer(
                id=c.id,
                cliente=cliente_nombre,
                fecha_inicio=c.fecha_inicio.isoformat(),
                fecha_fin=c.fecha_fin.isoformat(),
                monto_mensual=c.monto_mensual,
                estado=c.estado.value if hasattr(c.estado, "value") else str(c.estado),
                dias_restantes=dias_restantes,
            ))
        return result
