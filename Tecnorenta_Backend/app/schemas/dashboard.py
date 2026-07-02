from typing import Literal

from pydantic import BaseModel

Semaforo = Literal["verde", "ambar", "rojo", "info"]
Categoria = Literal["Financiero", "Operativo", "Riesgo", "Comercial"]
Unidad = Literal["moneda", "porcentaje", "numero", "anios"]
Severidad = Literal["alta", "media", "baja"]


class DashboardStats(BaseModel):
    """Panel operativo (retrocompatible) + métricas de decisión agregadas."""
    # --- Conteos base (existentes) ---
    usuarios_count: int = 0
    clientes_count: int = 0
    activos_count: int = 0
    activos_por_estado: dict[str, int] = {}
    contratos_count: int = 0
    contratos_por_estado: dict[str, int] = {}
    contratos_proximos_vencer: int = 0
    mantenimientos_pendientes: int = 0
    incidencias_abiertas: int = 0
    pagos_vencidos: int = 0
    total_ingresos_mensuales: float = 0.0

    # --- Flota / ocupación ---
    activos_operativos: int = 0
    activos_rentados: int = 0
    ocupacion_flota: float = 0.0            # %
    valor_flota_depreciado: float = 0.0
    edad_promedio_flota_anios: float = 0.0

    # --- Ingreso recurrente ---
    mrr: float = 0.0
    arr: float = 0.0
    ingreso_en_riesgo_vencimientos: float = 0.0

    # --- Cobranza / cartera ---
    monto_facturado: float = 0.0
    monto_pagado: float = 0.0
    cartera_vencida: float = 0.0
    monto_pendiente: float = 0.0
    tasa_cobro: float = 0.0                 # %
    morosidad_pct: float = 0.0              # %
    pagos_totales: int = 0
    contratos_con_cartera_vencida: int = 0
    pagos_por_estado: dict[str, int] = {}

    # --- Comercial / churn ---
    contratos_cancelados: int = 0
    churn_pct: float = 0.0                  # %

    # --- Mantenimiento ---
    costo_mantenimiento_total: float = 0.0
    costo_mantenimiento_preventivo: float = 0.0
    costo_mantenimiento_correctivo: float = 0.0
    costo_mantenimiento_por_activo: float = 0.0
    mantenimientos_preventivos: int = 0
    mantenimientos_correctivos: int = 0
    mantenimientos_por_tipo: dict[str, int] = {}

    # --- Incidencias ---
    incidencias_por_gravedad: dict[str, int] = {}
    incidencias_graves_abiertas: int = 0


class KpiCard(BaseModel):
    """Ficha de KPI lista para render: número + meta + semáforo + tendencia."""
    clave: str
    nombre: str
    categoria: Categoria
    valor: float
    unidad: Unidad
    meta: float | None = None
    semaforo: Semaforo = "info"
    # variación % vs. período anterior (positiva = subió); None si no aplica
    tendencia_pct: float | None = None
    # "sube" | "baja" | "estable"; interpretación depende del KPI
    tendencia_direccion: Literal["sube", "baja", "estable"] | None = None
    # True cuando "subir" es bueno (ingresos), False cuando "subir" es malo (morosidad)
    mejor_arriba: bool = True
    descripcion: str = ""
    decision: str = ""


class KpisResponse(BaseModel):
    generado: str                     # ISO date de cálculo
    salud: list[KpiCard] = []         # franja superior (financiero/estratégico)
    operacion: list[KpiCard] = []     # franja media (operativo/riesgo)


class Recomendacion(BaseModel):
    id: str
    severidad: Severidad
    titulo: str
    detalle: str
    kpi_asociado: str
    accion: str
    ruta: str | None = None           # ruta del front sugerida para actuar


class PuntoTendencia(BaseModel):
    periodo: str                      # "YYYY-MM"
    mrr: float
    cobrado: float


class TendenciasResponse(BaseModel):
    serie: list[PuntoTendencia] = []
    mrr_actual: float = 0.0
    mrr_anterior: float = 0.0
    delta_pct: float = 0.0


class ActivoReporte(BaseModel):
    id: int
    modelo: str
    codigo_inventario: str
    estado: str
    total_contratos: int = 0
    ingresos_generados: float = 0.0


class ContratoProximoVencer(BaseModel):
    id: int
    cliente: str
    fecha_inicio: str
    fecha_fin: str
    monto_mensual: float
    estado: str
    dias_restantes: int
