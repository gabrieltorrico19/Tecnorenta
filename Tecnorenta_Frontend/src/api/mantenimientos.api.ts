import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Mantenimiento {
  id: number;
  tipo: string;                      // "preventivo" | "correctivo"
  fecha: string;
  costo: number;
  descripcion: string | null;
  url_foto: string | null;
  id_activo: number;
  frecuencia_dias: number | null;
  proxima_fecha: string | null;
  id_reporte_origen: number | null;
  tiempo_reparacion: number | null;
}

export interface MantenimientoCreate {
  tipo: string;
  fecha: string;
  costo?: number;
  descripcion?: string;
  url_foto?: string;
  id_activo: number;
  frecuencia_dias?: number | null;
  proxima_fecha?: string | null;
  id_reporte_origen?: number | null;
  tiempo_reparacion?: number | null;
}

export interface MantenimientoUpdate {
  costo?: number;
  descripcion?: string;
  url_foto?: string;
  proxima_fecha?: string | null;
  tiempo_reparacion?: number | null;
}

export interface MantenimientoFiltros extends PageParams {
  tipo?: string;
  id_activo?: number;
  fecha_desde?: string;
  fecha_hasta?: string;
}

export const mantenimientosApi = {
  listar: (params?: MantenimientoFiltros) => api.get<Page<Mantenimiento>>(ENDPOINTS.MANTENIMIENTOS, { params }),
  listarTodos: () => fetchAllPages<Mantenimiento>((p) => api.get<Page<Mantenimiento>>(ENDPOINTS.MANTENIMIENTOS, { params: p })),
  obtener: (id: number) => api.get<Mantenimiento>(`${ENDPOINTS.MANTENIMIENTOS}/${id}`),
  crear: (data: MantenimientoCreate) => api.post<Mantenimiento>(ENDPOINTS.MANTENIMIENTOS, data),
  actualizar: (id: number, data: MantenimientoUpdate) =>
    api.patch<Mantenimiento>(`${ENDPOINTS.MANTENIMIENTOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.MANTENIMIENTOS}/${id}`),
};
