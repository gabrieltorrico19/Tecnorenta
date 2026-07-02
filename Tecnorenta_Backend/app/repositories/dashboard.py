"""Repositorio de agregaciones para el DSS.

Encapsula las consultas SQL/ORM de solo lectura que alimentan al
DashboardService. No contiene reglas de negocio (semáforos, metas ni
recomendaciones): eso vive en la capa de servicio.
"""
import calendar
from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.activo import Activo, EstadoActivo
from app.models.contrato import Contrato, EstadoContrato
from app.models.pago import Pago, EstadoPago
from app.models.asignacion_activo import AsignacionActivo
from app.models.reporte_incidencia import ReporteIncidencia, EstadoIncidencia
from app.models.mantenimiento import Mantenimiento, TipoMantenimiento

# Estados de contrato que representan ingreso recurrente "en vigor": activo o
# renovado (en curso). Se excluyen vencido y cancelado porque ya no facturan.
# Se usa la MISMA definición en mrr() y en mrr_por_mes() para que el MRR actual
# coincida con el último punto de la serie de tendencias.
_ESTADOS_VIGENTES = (EstadoContrato.ACTIVO, EstadoContrato.RENOVADO)


def _enum_val(x) -> str:
    return x.value if hasattr(x, "value") else str(x)


def _month_bounds(anchor: date, offset: int) -> tuple[date, date]:
    """Devuelve (primer_dia, ultimo_dia) del mes desplazado `offset` meses."""
    m = anchor.month - 1 + offset
    y = anchor.year + m // 12
    m = m % 12 + 1
    return date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- conteos simples ----------
    def count_usuarios(self) -> int:
        return self.db.query(func.count(Usuario.id)).scalar() or 0

    def count_clientes(self) -> int:
        return self.db.query(func.count(Cliente.id)).scalar() or 0

    # ---------- flota ----------
    def activos_por_estado(self) -> dict[str, int]:
        rows = self.db.query(Activo.estado, func.count(Activo.id)).group_by(Activo.estado).all()
        return {_enum_val(estado): int(n) for estado, n in rows}

    def valor_y_edad_flota(self) -> tuple[float, float, int]:
        """(suma valor_depreciado, edad_promedio_anios, nº operativos) sobre
        activos no dados de baja."""
        activos = self.db.query(Activo.valor_depreciado, Activo.fecha_compra).filter(
            Activo.estado != EstadoActivo.BAJA
        ).all()
        hoy = date.today()
        total_valor = 0.0
        edades: list[float] = []
        for valor, fecha_compra in activos:
            total_valor += float(valor or 0.0)
            if fecha_compra:
                edades.append((hoy - fecha_compra).days / 365.25)
        edad_prom = round(sum(edades) / len(edades), 2) if edades else 0.0
        return round(total_valor, 2), edad_prom, len(activos)

    # ---------- contratos ----------
    def contratos_por_estado(self) -> dict[str, int]:
        rows = self.db.query(Contrato.estado, func.count(Contrato.id)).group_by(Contrato.estado).all()
        return {_enum_val(estado): int(n) for estado, n in rows}

    def mrr(self) -> float:
        total = self.db.query(func.coalesce(func.sum(Contrato.monto_mensual), 0)).filter(
            Contrato.estado.in_(_ESTADOS_VIGENTES)
        ).scalar() or 0.0
        return float(total)

    def contratos_proximos_vencer(self, dias: int = 30) -> list[Contrato]:
        hoy = date.today()
        return self.db.query(Contrato).filter(
            Contrato.estado == EstadoContrato.ACTIVO,
            Contrato.fecha_fin >= hoy,
            Contrato.fecha_fin <= hoy + timedelta(days=dias),
        ).order_by(Contrato.fecha_fin).all()

    def total_contratos(self) -> int:
        return self.db.query(func.count(Contrato.id)).scalar() or 0

    def contratos_cancelados(self) -> int:
        return self.db.query(func.count(Contrato.id)).filter(
            Contrato.estado == EstadoContrato.CANCELADO
        ).scalar() or 0

    # ---------- pagos / cobranza ----------
    def resumen_pagos(self) -> dict:
        rows = self.db.query(
            Pago.estado, func.count(Pago.id), func.coalesce(func.sum(Pago.monto), 0)
        ).group_by(Pago.estado).all()

        por_estado: dict[str, int] = {}
        montos: dict[str, float] = {}
        for estado, n, monto in rows:
            key = _enum_val(estado)
            por_estado[key] = int(n)
            montos[key] = float(monto)

        contratos_morosos = self.db.query(
            func.count(func.distinct(Pago.id_contrato))
        ).filter(Pago.estado == EstadoPago.VENCIDO).scalar() or 0

        facturado = sum(montos.values())
        pagado = montos.get("pagado", 0.0)
        vencido = montos.get("vencido", 0.0)
        pendiente = montos.get("pendiente", 0.0)
        total_count = sum(por_estado.values())
        vencido_count = por_estado.get("vencido", 0)

        # Tasa de cobro = cobrado sobre lo exigible (cobrado + vencido); las
        # cuotas aún no vencidas (pendiente) no penalizan el indicador.
        exigible = pagado + vencido
        tasa_cobro = round((pagado / exigible) * 100, 1) if exigible > 0 else 100.0
        morosidad = round((vencido_count / total_count) * 100, 1) if total_count > 0 else 0.0

        return {
            "por_estado": por_estado,
            "facturado": round(facturado, 2),
            "pagado": round(pagado, 2),
            "vencido": round(vencido, 2),
            "pendiente": round(pendiente, 2),
            "pagos_totales": total_count,
            "pagos_vencidos": vencido_count,
            "tasa_cobro": tasa_cobro,
            "morosidad_pct": morosidad,
            "contratos_con_cartera_vencida": int(contratos_morosos),
        }

    # ---------- mantenimiento ----------
    def resumen_mantenimiento(self) -> dict:
        rows = self.db.query(
            Mantenimiento.tipo, func.count(Mantenimiento.id), func.coalesce(func.sum(Mantenimiento.costo), 0)
        ).group_by(Mantenimiento.tipo).all()

        por_tipo: dict[str, int] = {}
        costos: dict[str, float] = {}
        for tipo, n, costo in rows:
            key = _enum_val(tipo)
            por_tipo[key] = int(n)
            costos[key] = float(costo)

        total = sum(costos.values())
        activos_count = self.db.query(func.count(Activo.id)).scalar() or 0
        costo_por_activo = round(total / activos_count, 2) if activos_count else 0.0
        return {
            "por_tipo": por_tipo,
            "costo_total": round(total, 2),
            "costo_preventivo": round(costos.get("preventivo", 0.0), 2),
            "costo_correctivo": round(costos.get("correctivo", 0.0), 2),
            "costo_por_activo": costo_por_activo,
            "preventivos": por_tipo.get("preventivo", 0),
            "correctivos": por_tipo.get("correctivo", 0),
        }

    def mantenimientos_programados(self, dias: int = 30) -> int:
        """Preventivos cuya próxima fecha cae dentro del horizonte (accionable)."""
        hoy = date.today()
        return self.db.query(func.count(Mantenimiento.id)).filter(
            Mantenimiento.proxima_fecha.isnot(None),
            Mantenimiento.proxima_fecha >= hoy,
            Mantenimiento.proxima_fecha <= hoy + timedelta(days=dias),
        ).scalar() or 0

    # ---------- incidencias ----------
    def resumen_incidencias(self) -> dict:
        por_gravedad_rows = self.db.query(
            ReporteIncidencia.gravedad, func.count(ReporteIncidencia.id)
        ).filter(ReporteIncidencia.estado != EstadoIncidencia.CERRADO).group_by(
            ReporteIncidencia.gravedad
        ).all()
        por_gravedad = {_enum_val(g): int(n) for g, n in por_gravedad_rows}
        abiertas = sum(por_gravedad.values())
        graves = por_gravedad.get("grave", 0)
        return {
            "por_gravedad": por_gravedad,
            "abiertas": abiertas,
            "graves_abiertas": graves,
        }

    # ---------- tendencias ----------
    def mrr_por_mes(self, meses: int = 6) -> list[tuple[str, float]]:
        """Reconstruye el MRR de cada mes a partir de la vigencia de los
        contratos (fecha_inicio..fecha_fin) que solapan ese mes."""
        hoy = date.today()
        contratos = self.db.query(
            Contrato.fecha_inicio, Contrato.fecha_fin, Contrato.monto_mensual, Contrato.estado
        ).filter(Contrato.estado.in_(_ESTADOS_VIGENTES)).all()

        serie: list[tuple[str, float]] = []
        for offset in range(-(meses - 1), 1):
            inicio, fin = _month_bounds(hoy, offset)
            total = sum(
                float(m) for ini, f, m, _ in contratos
                if ini <= fin and f >= inicio
            )
            serie.append((f"{inicio.year}-{inicio.month:02d}", round(total, 2)))
        return serie

    def cobrado_por_mes(self, meses: int = 6) -> dict[str, float]:
        hoy = date.today()
        primer_mes, _ = _month_bounds(hoy, -(meses - 1))
        rows = self.db.query(Pago.fecha, Pago.monto).filter(
            Pago.estado == EstadoPago.PAGADO,
            Pago.fecha >= primer_mes,
        ).all()
        acc: dict[str, float] = {}
        for fecha, monto in rows:
            key = f"{fecha.year}-{fecha.month:02d}"
            acc[key] = acc.get(key, 0.0) + float(monto)
        return acc

    # ---------- revenue per asset ----------
    def revenue_per_asset(self, limit: int = 10) -> list[dict]:
        rows = self.db.query(
            Activo.id, Activo.modelo, Activo.codigo_inventario, Activo.estado,
            AsignacionActivo.id_contrato, Contrato.monto_mensual,
        ).outerjoin(
            AsignacionActivo, AsignacionActivo.id_activo == Activo.id
        ).outerjoin(
            Contrato, Contrato.id == AsignacionActivo.id_contrato
        ).all()

        acc: dict[int, dict] = {}
        for act_id, modelo, codigo, estado, id_contrato, monto in rows:
            entry = acc.setdefault(act_id, {
                "id": act_id,
                "modelo": modelo,
                "codigo_inventario": codigo,
                "estado": _enum_val(estado),
                "_contratos": set(),
                "ingresos_generados": 0.0,
            })
            if id_contrato is not None and id_contrato not in entry["_contratos"]:
                entry["_contratos"].add(id_contrato)
                entry["ingresos_generados"] += float(monto or 0.0)

        salida = []
        for e in acc.values():
            salida.append({
                "id": e["id"],
                "modelo": e["modelo"],
                "codigo_inventario": e["codigo_inventario"],
                "estado": e["estado"],
                "total_contratos": len(e["_contratos"]),
                "ingresos_generados": round(e["ingresos_generados"], 2),
            })
        salida.sort(key=lambda x: x["ingresos_generados"], reverse=True)
        return salida[:limit]
