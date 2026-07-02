import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface DashboardStats {
  // conteos base
  usuarios_count: number;
  clientes_count: number;
  activos_count: number;
  activos_por_estado: Record<string, number>;
  contratos_count: number;
  contratos_por_estado: Record<string, number>;
  contratos_proximos_vencer: number;
  mantenimientos_pendientes: number;
  incidencias_abiertas: number;
  pagos_vencidos: number;
  total_ingresos_mensuales: number;
  // flota
  activos_operativos: number;
  activos_rentados: number;
  ocupacion_flota: number;
  valor_flota_depreciado: number;
  edad_promedio_flota_anios: number;
  // ingreso recurrente
  mrr: number;
  arr: number;
  ingreso_en_riesgo_vencimientos: number;
  // cobranza
  monto_facturado: number;
  monto_pagado: number;
  cartera_vencida: number;
  monto_pendiente: number;
  tasa_cobro: number;
  morosidad_pct: number;
  pagos_totales: number;
  contratos_con_cartera_vencida: number;
  pagos_por_estado: Record<string, number>;
  // comercial
  contratos_cancelados: number;
  churn_pct: number;
  // mantenimiento
  costo_mantenimiento_total: number;
  costo_mantenimiento_preventivo: number;
  costo_mantenimiento_correctivo: number;
  costo_mantenimiento_por_activo: number;
  mantenimientos_preventivos: number;
  mantenimientos_correctivos: number;
  mantenimientos_por_tipo: Record<string, number>;
  // incidencias
  incidencias_por_gravedad: Record<string, number>;
  incidencias_graves_abiertas: number;
}

export type Semaforo = "verde" | "ambar" | "rojo" | "info";
export type Unidad = "moneda" | "porcentaje" | "numero" | "anios";

export interface KpiCard {
  clave: string;
  nombre: string;
  categoria: "Financiero" | "Operativo" | "Riesgo" | "Comercial";
  valor: number;
  unidad: Unidad;
  meta: number | null;
  semaforo: Semaforo;
  tendencia_pct: number | null;
  tendencia_direccion: "sube" | "baja" | "estable" | null;
  mejor_arriba: boolean;
  descripcion: string;
  decision: string;
}

export interface KpisResponse {
  generado: string;
  salud: KpiCard[];
  operacion: KpiCard[];
}

export interface Recomendacion {
  id: string;
  severidad: "alta" | "media" | "baja";
  titulo: string;
  detalle: string;
  kpi_asociado: string;
  accion: string;
  ruta: string | null;
}

export interface PuntoTendencia {
  periodo: string;
  mrr: number;
  cobrado: number;
}

export interface TendenciasResponse {
  serie: PuntoTendencia[];
  mrr_actual: number;
  mrr_anterior: number;
  delta_pct: number;
}

export interface ActivoReporte {
  id: number;
  modelo: string;
  codigo_inventario: string;
  estado: string;
  total_contratos: number;
  ingresos_generados: number;
}

export interface ContratoProximoVencer {
  id: number;
  cliente: string;
  fecha_inicio: string;
  fecha_fin: string;
  monto_mensual: number;
  estado: string;
  dias_restantes: number;
}

export const dashboardApi = {
  stats: () => api.get<DashboardStats>(ENDPOINTS.DASHBOARD.STATS),
  kpis: () => api.get<KpisResponse>(ENDPOINTS.DASHBOARD.KPIS),
  recomendaciones: () => api.get<Recomendacion[]>(ENDPOINTS.DASHBOARD.RECOMENDACIONES),
  tendencias: (meses = 6) =>
    api.get<TendenciasResponse>(ENDPOINTS.DASHBOARD.TENDENCIAS, { params: { meses } }),
  activosReporte: (limit = 10) =>
    api.get<ActivoReporte[]>(ENDPOINTS.DASHBOARD.ACTIVOS_REPORTE, { params: { limit } }),
  contratosProximosVencer: (dias: number = 30) =>
    api.get<ContratoProximoVencer[]>(ENDPOINTS.DASHBOARD.CONTRATOS_PROXIMOS, { params: { dias } }),
};
