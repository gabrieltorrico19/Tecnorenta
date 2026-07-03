"""Servicio del generador de informes.

Expone el catálogo de tipos de informe (con sus filtros y opciones), valida
los filtros recibidos y construye la respuesta: resumen de agregados +
columnas tipadas + filas. El mismo resultado alimenta la vista JSON y la
exportación CSV (una sola fuente de verdad).
"""
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activo import EstadoActivo
from app.models.contrato import EstadoContrato
from app.models.pago import EstadoPago
from app.models.mantenimiento import TipoMantenimiento
from app.models.reporte_incidencia import GravedadIncidencia, EstadoIncidencia
from app.repositories.informe import InformeRepository
from app.schemas.informe import (
    TipoInformeOut,
    FiltroInforme,
    OpcionFiltro,
    InformeOut,
    ResumenItem,
    ColumnaInforme,
)

# Máximo de filas devueltas en la vista JSON (el CSV exporta todo).
LIMITE_FILAS_JSON = 1000


def _opciones_enum(enum_cls) -> list[OpcionFiltro]:
    return [OpcionFiltro(value=e.value, label=e.value.replace("_", " ").capitalize()) for e in enum_cls]


def _parse_enum(enum_cls, valor: str | None, nombre_filtro: str):
    if valor is None or valor == "":
        return None
    try:
        return enum_cls(valor)
    except ValueError:
        validos = ", ".join(e.value for e in enum_cls)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Valor inválido para '{nombre_filtro}': use uno de [{validos}]",
        )


class InformeService:
    def __init__(self, db: Session):
        self.repo = InformeRepository(db)

    # ------------------------------------------------ catálogo
    def get_tipos(self) -> list[TipoInformeOut]:
        cat_ops = [OpcionFiltro(value=str(i), label=n) for i, n in self.repo.opciones_categorias()]
        cli_ops = [OpcionFiltro(value=str(i), label=n) for i, n in self.repo.opciones_clientes()]
        f_desde = FiltroInforme(key="fecha_desde", label="Desde", tipo="date")
        f_hasta = FiltroInforme(key="fecha_hasta", label="Hasta", tipo="date")

        return [
            TipoInformeOut(
                tipo="inventario_activos",
                nombre="Inventario de activos",
                descripcion="Flota completa con estado, categoría y valor depreciado.",
                filtros=[
                    FiltroInforme(key="estado", label="Estado", tipo="select", opciones=_opciones_enum(EstadoActivo)),
                    FiltroInforme(key="id_categoria", label="Categoría", tipo="select", opciones=cat_ops),
                ],
            ),
            TipoInformeOut(
                tipo="contratos",
                nombre="Cartera de contratos",
                descripcion="Contratos con cliente, vigencia, cuota mensual y estado.",
                filtros=[
                    FiltroInforme(key="estado", label="Estado", tipo="select", opciones=_opciones_enum(EstadoContrato)),
                    FiltroInforme(key="id_cliente", label="Cliente", tipo="select", opciones=cli_ops),
                ],
            ),
            TipoInformeOut(
                tipo="cobranza",
                nombre="Cobranza y pagos",
                descripcion="Cuotas facturadas con su estado; tasa de cobro del conjunto filtrado.",
                filtros=[
                    FiltroInforme(key="estado", label="Estado", tipo="select", opciones=_opciones_enum(EstadoPago)),
                    f_desde, f_hasta,
                ],
            ),
            TipoInformeOut(
                tipo="mantenimientos",
                nombre="Costos de mantenimiento",
                descripcion="Intervenciones preventivas y correctivas con su costo.",
                filtros=[
                    FiltroInforme(key="tipo_mantenimiento", label="Tipo", tipo="select", opciones=_opciones_enum(TipoMantenimiento)),
                    f_desde, f_hasta,
                ],
            ),
            TipoInformeOut(
                tipo="incidencias",
                nombre="Incidencias",
                descripcion="Reportes de incidencia por gravedad y estado.",
                filtros=[
                    FiltroInforme(key="gravedad", label="Gravedad", tipo="select", opciones=_opciones_enum(GravedadIncidencia)),
                    FiltroInforme(key="estado", label="Estado", tipo="select", opciones=_opciones_enum(EstadoIncidencia)),
                ],
            ),
            TipoInformeOut(
                tipo="utilizacion_activos",
                nombre="Utilización e ingreso por activo",
                descripcion="Contratos e ingreso generado por cada activo (revenue per asset).",
                filtros=[],
            ),
            TipoInformeOut(
                tipo="cartera_vencida",
                nombre="Cartera vencida por cliente",
                descripcion="Ingreso en riesgo: cuotas vencidas agrupadas por cliente.",
                filtros=[],
            ),
        ]

    # ------------------------------------------------ generación
    def generar(
        self,
        tipo: str,
        estado: str | None = None,
        gravedad: str | None = None,
        tipo_mantenimiento: str | None = None,
        id_categoria: int | None = None,
        id_cliente: int | None = None,
        fecha_desde: date | None = None,
        fecha_hasta: date | None = None,
        limite: int | None = LIMITE_FILAS_JSON,
    ) -> InformeOut:
        """Construye el informe. `limite=None` devuelve todas las filas (CSV)."""
        builders = {
            "inventario_activos": self._inventario_activos,
            "contratos": self._contratos,
            "cobranza": self._cobranza,
            "mantenimientos": self._mantenimientos,
            "incidencias": self._incidencias,
            "utilizacion_activos": self._utilizacion,
            "cartera_vencida": self._cartera,
        }
        builder = builders.get(tipo)
        if builder is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Informe desconocido: {tipo}")

        informe = builder(
            estado=estado,
            gravedad=gravedad,
            tipo_mantenimiento=tipo_mantenimiento,
            id_categoria=id_categoria,
            id_cliente=id_cliente,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
        informe.generado = date.today().isoformat()
        informe.total_filas = len(informe.filas)
        if limite is not None:
            informe.filas = informe.filas[:limite]
        return informe

    # ------------------------------------------------ builders
    def _inventario_activos(self, estado=None, id_categoria=None, **_) -> InformeOut:
        e = _parse_enum(EstadoActivo, estado, "estado")
        filas = self.repo.activos(estado=e, id_categoria=id_categoria)
        total_valor = round(sum(f["valor_depreciado"] for f in filas), 2)
        operativos = sum(1 for f in filas if f["estado"] != EstadoActivo.BAJA.value)
        rentados = sum(1 for f in filas if f["estado"] == EstadoActivo.RENTADO.value)
        return InformeOut(
            tipo="inventario_activos",
            titulo="Inventario de activos",
            generado="",
            filtros_aplicados=_filtros_str(estado=estado, id_categoria=id_categoria),
            resumen=[
                ResumenItem(etiqueta="Activos", valor=len(filas)),
                ResumenItem(etiqueta="Operativos (sin baja)", valor=operativos),
                ResumenItem(etiqueta="Rentados", valor=rentados),
                ResumenItem(etiqueta="Valor depreciado total", valor=total_valor, unidad="moneda"),
            ],
            columnas=[
                ColumnaInforme(key="codigo_inventario", label="Código"),
                ColumnaInforme(key="modelo", label="Modelo"),
                ColumnaInforme(key="categoria", label="Categoría"),
                ColumnaInforme(key="estado", label="Estado", unidad="badge"),
                ColumnaInforme(key="fecha_compra", label="F. compra", unidad="fecha"),
                ColumnaInforme(key="valor_depreciado", label="Valor depreciado", unidad="moneda"),
            ],
            filas=filas,
        )

    def _contratos(self, estado=None, id_cliente=None, **_) -> InformeOut:
        e = _parse_enum(EstadoContrato, estado, "estado")
        filas = self.repo.contratos(estado=e, id_cliente=id_cliente)
        ingreso = round(sum(f["monto_mensual"] for f in filas if f["estado"] in ("activo", "renovado")), 2)
        hoy = date.today().isoformat()
        en_30d = sum(
            1 for f in filas
            if f["estado"] == "activo" and f["fecha_fin"] and hoy <= f["fecha_fin"] <= _mas_dias(30)
        )
        return InformeOut(
            tipo="contratos",
            titulo="Cartera de contratos",
            generado="",
            filtros_aplicados=_filtros_str(estado=estado, id_cliente=id_cliente),
            resumen=[
                ResumenItem(etiqueta="Contratos", valor=len(filas)),
                ResumenItem(etiqueta="Ingreso mensual (vigentes)", valor=ingreso, unidad="moneda"),
                ResumenItem(etiqueta="Vencen en 30 días", valor=en_30d),
            ],
            columnas=[
                ColumnaInforme(key="id", label="ID", unidad="numero"),
                ColumnaInforme(key="cliente", label="Cliente"),
                ColumnaInforme(key="fecha_inicio", label="Inicio", unidad="fecha"),
                ColumnaInforme(key="fecha_fin", label="Fin", unidad="fecha"),
                ColumnaInforme(key="monto_mensual", label="Cuota mensual", unidad="moneda"),
                ColumnaInforme(key="estado", label="Estado", unidad="badge"),
            ],
            filas=filas,
        )

    def _cobranza(self, estado=None, fecha_desde=None, fecha_hasta=None, **_) -> InformeOut:
        e = _parse_enum(EstadoPago, estado, "estado")
        filas = self.repo.pagos(estado=e, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        pagado = round(sum(f["monto"] for f in filas if f["estado"] == "pagado"), 2)
        vencido = round(sum(f["monto"] for f in filas if f["estado"] == "vencido"), 2)
        pendiente = round(sum(f["monto"] for f in filas if f["estado"] == "pendiente"), 2)
        exigible = pagado + vencido
        tasa = round((pagado / exigible) * 100, 1) if exigible > 0 else 100.0
        return InformeOut(
            tipo="cobranza",
            titulo="Cobranza y pagos",
            generado="",
            filtros_aplicados=_filtros_str(estado=estado, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta),
            resumen=[
                ResumenItem(etiqueta="Facturado", valor=round(pagado + vencido + pendiente, 2), unidad="moneda"),
                ResumenItem(etiqueta="Cobrado", valor=pagado, unidad="moneda"),
                ResumenItem(etiqueta="Vencido", valor=vencido, unidad="moneda"),
                ResumenItem(etiqueta="Pendiente", valor=pendiente, unidad="moneda"),
                ResumenItem(etiqueta="Tasa de cobro", valor=tasa, unidad="porcentaje"),
            ],
            columnas=[
                ColumnaInforme(key="cliente", label="Cliente"),
                ColumnaInforme(key="contrato", label="Contrato"),
                ColumnaInforme(key="concepto", label="Concepto"),
                ColumnaInforme(key="fecha", label="Fecha", unidad="fecha"),
                ColumnaInforme(key="monto", label="Monto", unidad="moneda"),
                ColumnaInforme(key="estado", label="Estado", unidad="badge"),
            ],
            filas=filas,
        )

    def _mantenimientos(self, tipo_mantenimiento=None, fecha_desde=None, fecha_hasta=None, **_) -> InformeOut:
        t = _parse_enum(TipoMantenimiento, tipo_mantenimiento, "tipo_mantenimiento")
        filas = self.repo.mantenimientos(tipo=t, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        total = round(sum(f["costo"] for f in filas), 2)
        prev = round(sum(f["costo"] for f in filas if f["tipo"] == "preventivo"), 2)
        corr = round(sum(f["costo"] for f in filas if f["tipo"] == "correctivo"), 2)
        return InformeOut(
            tipo="mantenimientos",
            titulo="Costos de mantenimiento",
            generado="",
            filtros_aplicados=_filtros_str(tipo=tipo_mantenimiento, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta),
            resumen=[
                ResumenItem(etiqueta="Intervenciones", valor=len(filas)),
                ResumenItem(etiqueta="Costo total", valor=total, unidad="moneda"),
                ResumenItem(etiqueta="Preventivo", valor=prev, unidad="moneda"),
                ResumenItem(etiqueta="Correctivo", valor=corr, unidad="moneda"),
            ],
            columnas=[
                ColumnaInforme(key="activo", label="Activo"),
                ColumnaInforme(key="tipo", label="Tipo", unidad="badge"),
                ColumnaInforme(key="fecha", label="Fecha", unidad="fecha"),
                ColumnaInforme(key="costo", label="Costo", unidad="moneda"),
                ColumnaInforme(key="descripcion", label="Descripción"),
            ],
            filas=filas,
        )

    def _incidencias(self, gravedad=None, estado=None, **_) -> InformeOut:
        g = _parse_enum(GravedadIncidencia, gravedad, "gravedad")
        e = _parse_enum(EstadoIncidencia, estado, "estado")
        filas = self.repo.incidencias(gravedad=g, estado=e)
        abiertas = sum(1 for f in filas if f["estado"] != "cerrado")
        graves = sum(1 for f in filas if f["gravedad"] == "grave" and f["estado"] != "cerrado")
        return InformeOut(
            tipo="incidencias",
            titulo="Incidencias",
            generado="",
            filtros_aplicados=_filtros_str(gravedad=gravedad, estado=estado),
            resumen=[
                ResumenItem(etiqueta="Incidencias", valor=len(filas)),
                ResumenItem(etiqueta="Abiertas", valor=abiertas),
                ResumenItem(etiqueta="Graves abiertas", valor=graves),
            ],
            columnas=[
                ColumnaInforme(key="activo", label="Activo"),
                ColumnaInforme(key="fecha", label="Fecha", unidad="fecha"),
                ColumnaInforme(key="gravedad", label="Gravedad", unidad="badge"),
                ColumnaInforme(key="estado", label="Estado", unidad="badge"),
                ColumnaInforme(key="descripcion", label="Descripción"),
            ],
            filas=filas,
        )

    def _utilizacion(self, **_) -> InformeOut:
        filas = self.repo.utilizacion_activos()
        con_contrato = sum(1 for f in filas if f["total_contratos"] > 0)
        ingreso_total = round(sum(f["ingresos_generados"] for f in filas), 2)
        top = filas[0]["codigo_inventario"] if filas else "—"
        return InformeOut(
            tipo="utilizacion_activos",
            titulo="Utilización e ingreso por activo",
            generado="",
            resumen=[
                ResumenItem(etiqueta="Activos con contrato", valor=con_contrato),
                ResumenItem(etiqueta="Ingreso total generado", valor=ingreso_total, unidad="moneda"),
                ResumenItem(etiqueta="Activo top", valor=top, unidad="texto"),
            ],
            columnas=[
                ColumnaInforme(key="codigo_inventario", label="Código"),
                ColumnaInforme(key="modelo", label="Modelo"),
                ColumnaInforme(key="estado", label="Estado", unidad="badge"),
                ColumnaInforme(key="total_contratos", label="Contratos", unidad="numero"),
                ColumnaInforme(key="ingresos_generados", label="Ingreso generado", unidad="moneda"),
            ],
            filas=filas,
        )

    def _cartera(self, **_) -> InformeOut:
        filas = self.repo.cartera_vencida()
        total = round(sum(f["monto_vencido"] for f in filas), 2)
        cuotas = sum(f["cuotas_vencidas"] for f in filas)
        return InformeOut(
            tipo="cartera_vencida",
            titulo="Cartera vencida por cliente",
            generado="",
            resumen=[
                ResumenItem(etiqueta="Cartera vencida", valor=total, unidad="moneda"),
                ResumenItem(etiqueta="Clientes afectados", valor=len(filas)),
                ResumenItem(etiqueta="Cuotas vencidas", valor=cuotas),
            ],
            columnas=[
                ColumnaInforme(key="cliente", label="Cliente"),
                ColumnaInforme(key="contratos_afectados", label="Contratos", unidad="numero"),
                ColumnaInforme(key="cuotas_vencidas", label="Cuotas vencidas", unidad="numero"),
                ColumnaInforme(key="monto_vencido", label="Monto vencido", unidad="moneda"),
            ],
            filas=filas,
        )


def _mas_dias(dias: int) -> str:
    from datetime import timedelta
    return (date.today() + timedelta(days=dias)).isoformat()


def _filtros_str(**kwargs) -> dict[str, str]:
    return {k: str(v) for k, v in kwargs.items() if v is not None and v != ""}
