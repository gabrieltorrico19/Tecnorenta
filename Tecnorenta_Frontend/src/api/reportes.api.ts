import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Reporte {
  id: number;
  fecha: string;
  descripcion: string;
  gravedad: string;                  // "leve" | "moderado" | "grave"
  url_foto: string | null;
  estado: string;                    // "abierto" | "en_atencion" | "cerrado"
  id_activo: number;
}

export interface ReporteCreate {
  fecha: string;
  descripcion: string;
  gravedad: string;
  url_foto?: string;
  estado?: string;
  id_activo: number;
}

export interface ReporteUpdate {
  descripcion?: string;
  gravedad?: string;
  url_foto?: string;
  estado?: string;
}

export interface ReporteFiltros extends PageParams {
  gravedad?: string;
  estado?: string;
  id_activo?: number;
}

export const reportesApi = {
  listar: (params?: ReporteFiltros) => api.get<Page<Reporte>>(ENDPOINTS.REPORTES, { params }),
  listarTodos: () => fetchAllPages<Reporte>((p) => api.get<Page<Reporte>>(ENDPOINTS.REPORTES, { params: p })),
  obtener: (id: number) => api.get<Reporte>(`${ENDPOINTS.REPORTES}/${id}`),
  crear: (data: ReporteCreate) => api.post<Reporte>(ENDPOINTS.REPORTES, data),
  actualizar: (id: number, data: ReporteUpdate) =>
    api.patch<Reporte>(`${ENDPOINTS.REPORTES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.REPORTES}/${id}`),
};
