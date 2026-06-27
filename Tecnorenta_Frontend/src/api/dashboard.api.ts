import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface DashboardStats {
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
  contratosProximosVencer: (dias: number = 30) =>
    api.get<ContratoProximoVencer[]>(ENDPOINTS.DASHBOARD.CONTRATOS_PROXIMOS, { params: { dias } }),
};
