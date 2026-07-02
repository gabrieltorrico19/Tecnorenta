"""Servicio del DSS: transforma agregaciones en KPIs con semáforo/meta,
tendencias e recomendaciones automáticas por reglas de negocio.
"""
from datetime import date

from sqlalchemy.orm import Session

from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import (
    DashboardStats,
    KpiCard,
    KpisResponse,
    Recomendacion,
    PuntoTendencia,
    TendenciasResponse,
    ActivoReporte,
    ContratoProximoVencer,
)

# Orden de severidad para ordenar recomendaciones (mayor primero).
_ORDEN_SEV = {"alta": 0, "media": 1, "baja": 2}


def _pct(parte: float, total: float) -> float:
    return round((parte / total) * 100, 1) if total else 0.0


def _semaforo(valor: float, verde: float, ambar: float, mejor_arriba: bool = True) -> str:
    """Devuelve verde/ambar/rojo según umbrales.

    mejor_arriba=True  -> valores altos son buenos (ocupación, cobro).
    mejor_arriba=False -> valores altos son malos (morosidad, churn).
    """
    if mejor_arriba:
        if valor >= verde:
            return "verde"
        if valor >= ambar:
            return "ambar"
        return "rojo"
    else:
        if valor <= verde:
            return "verde"
        if valor <= ambar:
            return "ambar"
        return "rojo"


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DashboardRepository(db)

    # ------------------------------------------------------------------ #
    #  STATS (retrocompatible + métricas de decisión)
    # ------------------------------------------------------------------ #
    def get_stats(self) -> DashboardStats:
        activos_por_estado = self.repo.activos_por_estado()
        activos_count = sum(activos_por_estado.values())
        rentados = activos_por_estado.get("rentado", 0)
        baja = activos_por_estado.get("baja", 0)
        operativos = activos_count - baja
        ocupacion = _pct(rentados, operativos)
        valor_flota, edad_prom, _ = self.repo.valor_y_edad_flota()

        contratos_por_estado = self.repo.contratos_por_estado()
        contratos_count = sum(contratos_por_estado.values())
        mrr = self.repo.mrr()
        proximos = self.repo.contratos_proximos_vencer(30)
        ingreso_riesgo = round(sum(c.monto_mensual for c in proximos), 2)
        cancelados = self.repo.contratos_cancelados()
        churn = _pct(cancelados, contratos_count)

        pagos = self.repo.resumen_pagos()
        mant = self.repo.resumen_mantenimiento()
        mant_programados = self.repo.mantenimientos_programados(30)
        inc = self.repo.resumen_incidencias()

        return DashboardStats(
            usuarios_count=self.repo.count_usuarios(),
            clientes_count=self.repo.count_clientes(),
            activos_count=activos_count,
            activos_por_estado=activos_por_estado,
            contratos_count=contratos_count,
            contratos_por_estado=contratos_por_estado,
            contratos_proximos_vencer=len(proximos),
            mantenimientos_pendientes=mant_programados,
            incidencias_abiertas=inc["abiertas"],
            pagos_vencidos=pagos["pagos_vencidos"],
            total_ingresos_mensuales=mrr,
            # flota
            activos_operativos=operativos,
            activos_rentados=rentados,
            ocupacion_flota=ocupacion,
            valor_flota_depreciado=valor_flota,
            edad_promedio_flota_anios=edad_prom,
            # ingreso recurrente
            mrr=mrr,
            arr=round(mrr * 12, 2),
            ingreso_en_riesgo_vencimientos=ingreso_riesgo,
            # cobranza
            monto_facturado=pagos["facturado"],
            monto_pagado=pagos["pagado"],
            cartera_vencida=pagos["vencido"],
            monto_pendiente=pagos["pendiente"],
            tasa_cobro=pagos["tasa_cobro"],
            morosidad_pct=pagos["morosidad_pct"],
            pagos_totales=pagos["pagos_totales"],
            contratos_con_cartera_vencida=pagos["contratos_con_cartera_vencida"],
            pagos_por_estado=pagos["por_estado"],
            # comercial
            contratos_cancelados=cancelados,
            churn_pct=churn,
            # mantenimiento
            costo_mantenimiento_total=mant["costo_total"],
            costo_mantenimiento_preventivo=mant["costo_preventivo"],
            costo_mantenimiento_correctivo=mant["costo_correctivo"],
            costo_mantenimiento_por_activo=mant["costo_por_activo"],
            mantenimientos_preventivos=mant["preventivos"],
            mantenimientos_correctivos=mant["correctivos"],
            mantenimientos_por_tipo=mant["por_tipo"],
            # incidencias
            incidencias_por_gravedad=inc["por_gravedad"],
            incidencias_graves_abiertas=inc["graves_abiertas"],
        )

    # ------------------------------------------------------------------ #
    #  TENDENCIAS
    # ------------------------------------------------------------------ #
    def get_tendencias(self, meses: int = 6) -> TendenciasResponse:
        serie_mrr = self.repo.mrr_por_mes(meses)
        cobrado = self.repo.cobrado_por_mes(meses)
        serie = [
            PuntoTendencia(periodo=periodo, mrr=mrr, cobrado=round(cobrado.get(periodo, 0.0), 2))
            for periodo, mrr in serie_mrr
        ]
        mrr_actual = serie[-1].mrr if serie else 0.0
        mrr_anterior = serie[-2].mrr if len(serie) >= 2 else 0.0
        delta = _pct(mrr_actual - mrr_anterior, mrr_anterior) if mrr_anterior else 0.0
        return TendenciasResponse(
            serie=serie,
            mrr_actual=mrr_actual,
            mrr_anterior=mrr_anterior,
            delta_pct=delta,
        )

    # ------------------------------------------------------------------ #
    #  KPIs (fichas con semáforo/meta/tendencia)
    # ------------------------------------------------------------------ #
    def get_kpis(self) -> KpisResponse:
        s = self.get_stats()
        t = self.get_tendencias(6)
        dir_mrr = "sube" if t.delta_pct > 0.5 else "baja" if t.delta_pct < -0.5 else "estable"

        salud = [
            KpiCard(
                clave="mrr", nombre="Ingreso recurrente mensual (MRR)", categoria="Financiero",
                valor=s.mrr, unidad="moneda", meta=round(t.mrr_anterior, 2),
                semaforo=_semaforo(t.delta_pct, 0, -5, mejor_arriba=True),
                tendencia_pct=t.delta_pct, tendencia_direccion=dir_mrr, mejor_arriba=True,
                descripcion="Suma del monto mensual de los contratos activos. ARR = MRR × 12.",
                decision="Si cae vs. mes anterior, revisar renovaciones y nuevas altas.",
            ),
            KpiCard(
                clave="ocupacion_flota", nombre="Ocupación de flota", categoria="Operativo",
                valor=s.ocupacion_flota, unidad="porcentaje", meta=70,
                semaforo=_semaforo(s.ocupacion_flota, 70, 55, mejor_arriba=True),
                mejor_arriba=True,
                descripcion=f"{s.activos_rentados} rentados / {s.activos_operativos} operativos (excluye baja).",
                decision="Bajo la meta: activar campaña comercial o revisar precios.",
            ),
            KpiCard(
                clave="tasa_cobro", nombre="Tasa de cobro", categoria="Financiero",
                valor=s.tasa_cobro, unidad="porcentaje", meta=90,
                semaforo=_semaforo(s.tasa_cobro, 90, 75, mejor_arriba=True),
                mejor_arriba=True,
                descripcion="Cobrado / (cobrado + vencido). No penaliza cuotas aún no vencidas.",
                decision="Bajo meta: intensificar gestión de cobranza.",
            ),
            KpiCard(
                clave="cartera_vencida", nombre="Cartera vencida (ingreso en riesgo)", categoria="Riesgo",
                valor=s.cartera_vencida, unidad="moneda", meta=0,
                semaforo=("verde" if s.cartera_vencida == 0
                          else "ambar" if s.cartera_vencida <= 0.10 * s.monto_facturado
                          else "rojo"),
                mejor_arriba=False,
                descripcion=f"Suma de cuotas vencidas en {s.contratos_con_cartera_vencida} contrato(s).",
                decision="Priorizar cobranza de los contratos morosos.",
            ),
            KpiCard(
                clave="ingreso_en_riesgo", nombre="Ingreso en riesgo por vencimientos", categoria="Riesgo",
                valor=s.ingreso_en_riesgo_vencimientos, unidad="moneda", meta=0,
                semaforo=("verde" if s.ingreso_en_riesgo_vencimientos == 0
                          else "ambar" if s.ingreso_en_riesgo_vencimientos <= 0.20 * s.mrr
                          else "rojo"),
                mejor_arriba=False,
                descripcion=f"MRR de {s.contratos_proximos_vencer} contrato(s) que vencen en 30 días.",
                decision="Contactar clientes para renovación antes del vencimiento.",
            ),
            KpiCard(
                clave="churn", nombre="Churn de contratos", categoria="Comercial",
                valor=s.churn_pct, unidad="porcentaje", meta=10,
                semaforo=_semaforo(s.churn_pct, 10, 15, mejor_arriba=False),
                mejor_arriba=False,
                descripcion=f"{s.contratos_cancelados} cancelados / {s.contratos_count} contratos.",
                decision="Sobre meta: analizar causas de cancelación y retención.",
            ),
        ]

        correctivo_pct = _pct(s.costo_mantenimiento_correctivo, s.costo_mantenimiento_total)
        operacion = [
            KpiCard(
                clave="morosidad", nombre="Morosidad", categoria="Riesgo",
                valor=s.morosidad_pct, unidad="porcentaje", meta=10,
                semaforo=_semaforo(s.morosidad_pct, 10, 20, mejor_arriba=False),
                mejor_arriba=False,
                descripcion="Cuotas vencidas / cuotas totales.",
                decision="Sobre meta: reforzar recordatorios y política de cobro.",
            ),
            KpiCard(
                clave="correctivo_pct", nombre="Peso del mantenimiento correctivo", categoria="Operativo",
                valor=correctivo_pct, unidad="porcentaje", meta=40,
                semaforo=_semaforo(correctivo_pct, 40, 60, mejor_arriba=False),
                mejor_arriba=False,
                descripcion=f"Correctivo {s.costo_mantenimiento_correctivo:.0f} de {s.costo_mantenimiento_total:.0f} total.",
                decision="Alto: reforzar plan preventivo para reducir fallas.",
            ),
            KpiCard(
                clave="incidencias_abiertas", nombre="Incidencias abiertas", categoria="Operativo",
                valor=s.incidencias_abiertas, unidad="numero", meta=0,
                semaforo=("rojo" if s.incidencias_graves_abiertas > 0
                          else "ambar" if s.incidencias_abiertas > 0 else "verde"),
                mejor_arriba=False,
                descripcion=f"{s.incidencias_graves_abiertas} grave(s) sin cerrar.",
                decision="Graves abiertas: atención técnica inmediata.",
            ),
            KpiCard(
                clave="mant_programados", nombre="Mantenimientos programados (30d)", categoria="Operativo",
                valor=s.mantenimientos_pendientes, unidad="numero", meta=None,
                semaforo="info", mejor_arriba=True,
                descripcion="Preventivos con próxima fecha dentro de 30 días.",
                decision="Agendar técnico para no perder la ventana preventiva.",
            ),
            KpiCard(
                clave="valor_flota", nombre="Valor depreciado de flota", categoria="Financiero",
                valor=s.valor_flota_depreciado, unidad="moneda", meta=None,
                semaforo="info", mejor_arriba=True,
                descripcion="Suma de valor_depreciado de activos operativos.",
                decision="Base para decisiones de renovación/reposición de equipos.",
            ),
            KpiCard(
                clave="edad_flota", nombre="Edad promedio de flota", categoria="Operativo",
                valor=s.edad_promedio_flota_anios, unidad="anios", meta=3,
                semaforo=_semaforo(s.edad_promedio_flota_anios, 3, 4, mejor_arriba=False),
                mejor_arriba=False,
                descripcion="Promedio de años desde fecha_compra (operativos).",
                decision="Flota envejecida: planificar reposición.",
            ),
        ]
        return KpisResponse(generado=date.today().isoformat(), salud=salud, operacion=operacion)

    # ------------------------------------------------------------------ #
    #  RECOMENDACIONES (reglas de negocio sobre los KPIs)
    # ------------------------------------------------------------------ #
    def get_recomendaciones(self) -> list[Recomendacion]:
        s = self.get_stats()
        recs: list[Recomendacion] = []

        if s.incidencias_graves_abiertas > 0:
            recs.append(Recomendacion(
                id="incidencias_graves", severidad="alta",
                titulo=f"{s.incidencias_graves_abiertas} incidencia(s) grave(s) abierta(s)",
                detalle="Hay activos con fallas graves sin cerrar que pueden dejar equipos fuera de servicio.",
                kpi_asociado="incidencias_abiertas",
                accion="Asignar técnico y abrir mantenimiento correctivo de inmediato.",
                ruta="/reportes",
            ))

        if s.cartera_vencida > 0:
            recs.append(Recomendacion(
                id="cartera_vencida", severidad="alta",
                titulo=f"Cartera vencida por {s.cartera_vencida:,.0f}",
                detalle=f"{s.contratos_con_cartera_vencida} contrato(s) con cuotas vencidas; "
                        f"tasa de cobro {s.tasa_cobro}% (meta 90%).",
                kpi_asociado="cartera_vencida",
                accion="Gestionar cobranza de los contratos morosos esta semana.",
                ruta="/pagos",
            ))

        if s.contratos_proximos_vencer > 0:
            recs.append(Recomendacion(
                id="vencimientos", severidad="alta" if s.ingreso_en_riesgo_vencimientos > 0.15 * s.mrr else "media",
                titulo=f"{s.contratos_proximos_vencer} contrato(s) vencen en 30 días",
                detalle=f"MRR en riesgo por {s.ingreso_en_riesgo_vencimientos:,.0f} si no se renuevan.",
                kpi_asociado="ingreso_en_riesgo",
                accion="Contactar a los clientes para renovación anticipada.",
                ruta="/contratos",
            ))

        if s.ocupacion_flota < 70:
            recs.append(Recomendacion(
                id="ocupacion", severidad="media",
                titulo=f"Ocupación de flota {s.ocupacion_flota}% bajo meta 70%",
                detalle=f"{s.activos_operativos - s.activos_rentados} equipo(s) operativos sin rentar generan costo sin ingreso.",
                kpi_asociado="ocupacion_flota",
                accion="Activar campaña comercial o revisar precios de los equipos disponibles.",
                ruta="/activos",
            ))

        if s.costo_mantenimiento_correctivo > s.costo_mantenimiento_preventivo:
            recs.append(Recomendacion(
                id="preventivo", severidad="media",
                titulo="El mantenimiento correctivo supera al preventivo",
                detalle=f"Correctivo {s.costo_mantenimiento_correctivo:,.0f} vs. preventivo "
                        f"{s.costo_mantenimiento_preventivo:,.0f}.",
                kpi_asociado="correctivo_pct",
                accion="Reforzar el plan preventivo para reducir fallas y costo reactivo.",
                ruta="/mantenimientos",
            ))

        if s.churn_pct > 10:
            recs.append(Recomendacion(
                id="churn", severidad="media",
                titulo=f"Churn {s.churn_pct}% sobre la meta de 10%",
                detalle=f"{s.contratos_cancelados} contrato(s) cancelado(s) de {s.contratos_count}.",
                kpi_asociado="churn",
                accion="Analizar causas de cancelación y diseñar plan de retención.",
                ruta="/contratos",
            ))

        if s.mantenimientos_pendientes > 0:
            recs.append(Recomendacion(
                id="mant_programados", severidad="baja",
                titulo=f"{s.mantenimientos_pendientes} mantenimiento(s) preventivo(s) por ejecutar",
                detalle="Preventivos con próxima fecha dentro de los próximos 30 días.",
                kpi_asociado="mant_programados",
                accion="Agendar al técnico dentro de la ventana preventiva.",
                ruta="/mantenimientos",
            ))

        if not recs:
            recs.append(Recomendacion(
                id="sin_alertas", severidad="baja",
                titulo="Sin alertas críticas",
                detalle="Todos los indicadores están dentro de los umbrales saludables.",
                kpi_asociado="general",
                accion="Mantener el seguimiento y foco en crecimiento comercial.",
                ruta="/",
            ))

        recs.sort(key=lambda r: _ORDEN_SEV.get(r.severidad, 9))
        return recs

    # ------------------------------------------------------------------ #
    #  Detalle: revenue per asset y contratos próximos a vencer
    # ------------------------------------------------------------------ #
    def get_activos_reporte(self, limit: int = 10) -> list[ActivoReporte]:
        return [ActivoReporte(**row) for row in self.repo.revenue_per_asset(limit)]

    def get_contratos_proximos_vencer(self, dias: int = 30) -> list[ContratoProximoVencer]:
        hoy = date.today()
        result: list[ContratoProximoVencer] = []
        for c in self.repo.contratos_proximos_vencer(dias):
            cliente_nombre = c.cliente.razon_social if c.cliente else "—"
            result.append(ContratoProximoVencer(
                id=c.id,
                cliente=cliente_nombre,
                fecha_inicio=c.fecha_inicio.isoformat(),
                fecha_fin=c.fecha_fin.isoformat(),
                monto_mensual=c.monto_mensual,
                estado=c.estado.value if hasattr(c.estado, "value") else str(c.estado),
                dias_restantes=(c.fecha_fin - hoy).days,
            ))
        return result
