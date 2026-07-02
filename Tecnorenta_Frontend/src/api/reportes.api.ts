import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Reporte {
  id: number;
  activo_id: number;
  activo_nombre?: string;
  usuario_id: number;
  usuario_nombre?: string;
  tipo_incidencia: string;
  descripcion: string;
  fecha_reporte: string;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface ReporteCreate {
  activo_id: number;
  usuario_id: number;
  tipo_incidencia: string;
  descripcion: string;
  fecha_reporte: string;
  estado: string;
}

export interface ReporteUpdate {
  tipo_incidencia?: string;
  descripcion?: string;
  estado?: string;
}

export const reportesApi = {
  listar: (params?: PageParams) => api.get<Page<Reporte>>(ENDPOINTS.REPORTES, { params }),
  listarTodos: () => fetchAllPages<Reporte>((p) => api.get<Page<Reporte>>(ENDPOINTS.REPORTES, { params: p })),
  obtener: (id: number) => api.get<Reporte>(`${ENDPOINTS.REPORTES}/${id}`),
  crear: (data: ReporteCreate) => api.post<Reporte>(ENDPOINTS.REPORTES, data),
  actualizar: (id: number, data: ReporteUpdate) =>
    api.patch<Reporte>(`${ENDPOINTS.REPORTES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.REPORTES}/${id}`),
};
