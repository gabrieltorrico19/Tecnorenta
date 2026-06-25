import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Rol {
  id: number;
  nombre: string;
  descripcion: string | null;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface RolCreate {
  nombre: string;
  descripcion?: string;
}

export interface RolUpdate {
  nombre?: string;
  descripcion?: string;
  activo?: boolean;
}

export const rolesApi = {
  listar: () => api.get<Rol[]>(ENDPOINTS.ROLES),
  obtener: (id: number) => api.get<Rol>(`${ENDPOINTS.ROLES}/${id}`),
  crear: (data: RolCreate) => api.post<Rol>(ENDPOINTS.ROLES, data),
  actualizar: (id: number, data: RolUpdate) =>
    api.patch<Rol>(`${ENDPOINTS.ROLES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.ROLES}/${id}`),
};
