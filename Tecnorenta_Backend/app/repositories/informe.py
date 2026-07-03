"""Repositorio de consultas para el generador de informes.

Devuelve filas ya "aplanadas" (dict) con los nombres de las entidades
relacionadas resueltos vía JOIN, listas para tabular o exportar a CSV.
No contiene formato ni reglas de presentación: eso vive en el servicio.
"""
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activo import Activo, EstadoActivo
from app.models.categoria_activo import CategoriaActivo
from app.models.cliente import Cliente
from app.models.contrato import Contrato, EstadoContrato
from app.models.pago import Pago, EstadoPago
from app.models.mantenimiento import Mantenimiento, TipoMantenimiento
from app.models.reporte_incidencia import ReporteIncidencia, GravedadIncidencia, EstadoIncidencia
from app.repositories.dashboard import DashboardRepository


def _val(x) -> str:
    return x.value if hasattr(x, "value") else str(x)


def _iso(d: date | None) -> str | None:
    return d.isoformat() if d else None


class InformeRepository:
    def __init__(self, db: Session):
        self.db = db
        self.dashboard = DashboardRepository(db)

    # ---------- catálogos para las opciones de filtro ----------
    def opciones_categorias(self) -> list[tuple[int, str]]:
        rows = self.db.query(CategoriaActivo.id, CategoriaActivo.nombre).order_by(CategoriaActivo.nombre).all()
        return [(int(i), n) for i, n in rows]

    def opciones_clientes(self) -> list[tuple[int, str]]:
        rows = self.db.query(Cliente.id, Cliente.razon_social).order_by(Cliente.razon_social).all()
        return [(int(i), n) for i, n in rows]

    # ---------- informes ----------
    def activos(self, estado: EstadoActivo | None = None, id_categoria: int | None = None) -> list[dict]:
        q = self.db.query(Activo, CategoriaActivo.nombre).outerjoin(
            CategoriaActivo, Activo.id_categoria == CategoriaActivo.id
        )
        if estado is not None:
            q = q.filter(Activo.estado == estado)
        if id_categoria is not None:
            q = q.filter(Activo.id_categoria == id_categoria)
        filas = []
        for a, cat_nombre in q.order_by(Activo.codigo_inventario).all():
            filas.append({
                "id": a.id,
                "codigo_inventario": a.codigo_inventario,
                "modelo": a.modelo,
                "categoria": cat_nombre or "—",
                "estado": _val(a.estado),
                "fecha_compra": _iso(a.fecha_compra),
                "valor_depreciado": float(a.valor_depreciado or 0.0),
            })
        return filas

    def contratos(self, estado: EstadoContrato | None = None, id_cliente: int | None = None) -> list[dict]:
        q = self.db.query(Contrato, Cliente.razon_social).join(
            Cliente, Contrato.id_cliente == Cliente.id
        )
        if estado is not None:
            q = q.filter(Contrato.estado == estado)
        if id_cliente is not None:
            q = q.filter(Contrato.id_cliente == id_cliente)
        filas = []
        for c, cliente in q.order_by(Contrato.fecha_fin).all():
            filas.append({
                "id": c.id,
                "cliente": cliente,
                "fecha_inicio": _iso(c.fecha_inicio),
                "fecha_fin": _iso(c.fecha_fin),
                "monto_mensual": float(c.monto_mensual),
                "estado": _val(c.estado),
            })
        return filas

    def pagos(
        self,
        estado: EstadoPago | None = None,
        fecha_desde: date | None = None,
        fecha_hasta: date | None = None,
    ) -> list[dict]:
        q = self.db.query(Pago, Contrato.id, Cliente.razon_social).join(
            Contrato, Pago.id_contrato == Contrato.id
        ).join(Cliente, Contrato.id_cliente == Cliente.id)
        if estado is not None:
            q = q.filter(Pago.estado == estado)
        if fecha_desde is not None:
            q = q.filter(Pago.fecha >= fecha_desde)
        if fecha_hasta is not None:
            q = q.filter(Pago.fecha <= fecha_hasta)
        filas = []
        for p, id_contrato, cliente in q.order_by(Pago.fecha.desc()).all():
            filas.append({
                "id": p.id,
                "cliente": cliente,
                "contrato": f"#{id_contrato}",
                "concepto": p.concepto,
                "fecha": _iso(p.fecha),
                "monto": float(p.monto),
                "estado": _val(p.estado),
            })
        return filas

    def mantenimientos(
        self,
        tipo: TipoMantenimiento | None = None,
        fecha_desde: date | None = None,
        fecha_hasta: date | None = None,
    ) -> list[dict]:
        q = self.db.query(Mantenimiento, Activo.codigo_inventario, Activo.modelo).join(
            Activo, Mantenimiento.id_activo == Activo.id
        )
        if tipo is not None:
            q = q.filter(Mantenimiento.tipo == tipo)
        if fecha_desde is not None:
            q = q.filter(Mantenimiento.fecha >= fecha_desde)
        if fecha_hasta is not None:
            q = q.filter(Mantenimiento.fecha <= fecha_hasta)
        filas = []
        for m, codigo, modelo in q.order_by(Mantenimiento.fecha.desc()).all():
            filas.append({
                "id": m.id,
                "activo": f"{codigo} · {modelo}",
                "tipo": _val(m.tipo),
                "fecha": _iso(m.fecha),
                "costo": float(m.costo or 0.0),
                "descripcion": m.descripcion or "—",
            })
        return filas

    def incidencias(
        self,
        gravedad: GravedadIncidencia | None = None,
        estado: EstadoIncidencia | None = None,
    ) -> list[dict]:
        q = self.db.query(ReporteIncidencia, Activo.codigo_inventario, Activo.modelo).join(
            Activo, ReporteIncidencia.id_activo == Activo.id
        )
        if gravedad is not None:
            q = q.filter(ReporteIncidencia.gravedad == gravedad)
        if estado is not None:
            q = q.filter(ReporteIncidencia.estado == estado)
        filas = []
        for r, codigo, modelo in q.order_by(ReporteIncidencia.fecha.desc()).all():
            filas.append({
                "id": r.id,
                "activo": f"{codigo} · {modelo}",
                "fecha": _iso(r.fecha),
                "gravedad": _val(r.gravedad),
                "estado": _val(r.estado),
                "descripcion": r.descripcion,
            })
        return filas

    def utilizacion_activos(self) -> list[dict]:
        # Reutiliza la agregación revenue-per-asset del DSS (contratos distintos
        # por activo vía asignaciones e ingreso generado).
        return self.dashboard.revenue_per_asset(limit=10_000)

    def cartera_vencida(self) -> list[dict]:
        rows = self.db.query(
            Cliente.id,
            Cliente.razon_social,
            func.count(func.distinct(Pago.id_contrato)),
            func.count(Pago.id),
            func.coalesce(func.sum(Pago.monto), 0),
        ).join(Contrato, Contrato.id_cliente == Cliente.id).join(
            Pago, Pago.id_contrato == Contrato.id
        ).filter(Pago.estado == EstadoPago.VENCIDO).group_by(
            Cliente.id, Cliente.razon_social
        ).order_by(func.coalesce(func.sum(Pago.monto), 0).desc()).all()

        return [{
            "id": int(cid),
            "cliente": nombre,
            "contratos_afectados": int(n_contratos),
            "cuotas_vencidas": int(n_cuotas),
            "monto_vencido": float(monto),
        } for cid, nombre, n_contratos, n_cuotas, monto in rows]
