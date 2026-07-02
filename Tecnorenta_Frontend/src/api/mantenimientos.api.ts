import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Mantenimiento {
  id: number;
  activo_id: number;
  activo_nombre?: string;
  tipo_mantenimiento: string;
  descripcion: string;
  fecha_inicio: string | null;
  fecha_fin: string | null;
  costo: number | null;
  proveedor: string | null;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface MantenimientoCreate {
  activo_id: number;
  tipo_mantenimiento: string;
  descripcion: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  costo?: number;
  proveedor?: string;
  estado: string;
}

export interface MantenimientoUpdate {
  tipo_mantenimiento?: string;
  descripcion?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  costo?: number;
  proveedor?: string;
  estado?: string;
}

export const mantenimientosApi = {
  listar: (params?: PageParams) => api.get<Page<Mantenimiento>>(ENDPOINTS.MANTENIMIENTOS, { params }),
  listarTodos: () => fetchAllPages<Mantenimiento>((p) => api.get<Page<Mantenimiento>>(ENDPOINTS.MANTENIMIENTOS, { params: p })),
  obtener: (id: number) => api.get<Mantenimiento>(`${ENDPOINTS.MANTENIMIENTOS}/${id}`),
  crear: (data: MantenimientoCreate) => api.post<Mantenimiento>(ENDPOINTS.MANTENIMIENTOS, data),
  actualizar: (id: number, data: MantenimientoUpdate) =>
    api.patch<Mantenimiento>(`${ENDPOINTS.MANTENIMIENTOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.MANTENIMIENTOS}/${id}`),
};
