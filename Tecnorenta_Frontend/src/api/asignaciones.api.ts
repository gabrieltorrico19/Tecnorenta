import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Asignacion {
  id: number;
  activo_id: number;
  activo_nombre?: string;
  usuario_id: number;
  usuario_nombre?: string;
  fecha_asignacion: string;
  fecha_devolucion: string | null;
  motivo: string | null;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface AsignacionCreate {
  activo_id: number;
  usuario_id: number;
  fecha_asignacion: string;
  fecha_devolucion?: string;
  motivo?: string;
  estado: string;
}

export interface AsignacionUpdate {
  fecha_devolucion?: string;
  motivo?: string;
  estado?: string;
}

export const asignacionesApi = {
  listar: () => api.get<Asignacion[]>(ENDPOINTS.ASIGNACIONES),
  obtener: (id: number) => api.get<Asignacion>(`${ENDPOINTS.ASIGNACIONES}/${id}`),
  crear: (data: AsignacionCreate) => api.post<Asignacion>(ENDPOINTS.ASIGNACIONES, data),
  actualizar: (id: number, data: AsignacionUpdate) =>
    api.patch<Asignacion>(`${ENDPOINTS.ASIGNACIONES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.ASIGNACIONES}/${id}`),
};
