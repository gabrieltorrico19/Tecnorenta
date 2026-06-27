import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Asignacion {
  id: number;
  fecha_asignacion: string;
  fecha_devolucion: string | null;
  latitud: number | null;
  longitud: number | null;
  id_contrato: number;
  id_activo: number;
}

export interface AsignacionCreate {
  fecha_asignacion: string;
  fecha_devolucion?: string;
  id_contrato: number;
  id_activo: number;
  latitud?: number | null;
  longitud?: number | null;
}

export interface AsignacionUpdate {
  fecha_devolucion?: string;
  latitud?: number | null;
  longitud?: number | null;
}

export const asignacionesApi = {
  listar: () => api.get<Asignacion[]>(ENDPOINTS.ASIGNACIONES),
  obtener: (id: number) => api.get<Asignacion>(`${ENDPOINTS.ASIGNACIONES}/${id}`),
  crear: (data: AsignacionCreate) => api.post<Asignacion>(ENDPOINTS.ASIGNACIONES, data),
  actualizar: (id: number, data: AsignacionUpdate) =>
    api.patch<Asignacion>(`${ENDPOINTS.ASIGNACIONES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.ASIGNACIONES}/${id}`),
};
