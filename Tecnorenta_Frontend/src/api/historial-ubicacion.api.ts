import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface HistorialUbicacion {
  id: number;
  id_asignacion: number;
  latitud: number;
  longitud: number;
  timestamp: string | null;
}

export interface HistorialUbicacionCreate {
  id_asignacion: number;
  latitud: number;
  longitud: number;
}

export interface HistorialUbicacionUpdate {
  latitud?: number;
  longitud?: number;
}

export const historialUbicacionApi = {
  listar: (params?: PageParams) => api.get<Page<HistorialUbicacion>>(ENDPOINTS.HISTORIAL_UBICACION, { params }),
  listarTodos: () =>
    fetchAllPages<HistorialUbicacion>((p) => api.get<Page<HistorialUbicacion>>(ENDPOINTS.HISTORIAL_UBICACION, { params: p })),
  listarPorAsignacion: (asignacionId: number) =>
    api.get<HistorialUbicacion[]>(`${ENDPOINTS.HISTORIAL_UBICACION}/asignacion/${asignacionId}`),
  obtener: (id: number) => api.get<HistorialUbicacion>(`${ENDPOINTS.HISTORIAL_UBICACION}/${id}`),
  crear: (data: HistorialUbicacionCreate) => api.post<HistorialUbicacion>(ENDPOINTS.HISTORIAL_UBICACION, data),
  actualizar: (id: number, data: HistorialUbicacionUpdate) =>
    api.patch<HistorialUbicacion>(`${ENDPOINTS.HISTORIAL_UBICACION}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.HISTORIAL_UBICACION}/${id}`),
};
