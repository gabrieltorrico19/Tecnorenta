import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  telefono: string | null;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface UsuarioCreate {
  nombre: string;
  email: string;
  password: string;
  telefono?: string;
}

export interface UsuarioUpdate {
  nombre?: string;
  email?: string;
  password?: string;
  telefono?: string;
  activo?: boolean;
}

export const usuarioApi = {
  listar: (params?: PageParams) => api.get<Page<Usuario>>(ENDPOINTS.USUARIOS, { params }),
  listarTodos: () => fetchAllPages<Usuario>((p) => api.get<Page<Usuario>>(ENDPOINTS.USUARIOS, { params: p })),
  obtener: (id: number) => api.get<Usuario>(`${ENDPOINTS.USUARIOS}/${id}`),
  crear: (data: UsuarioCreate) => api.post<Usuario>(ENDPOINTS.USUARIOS, data),
  actualizar: (id: number, data: UsuarioUpdate) =>
    api.patch<Usuario>(`${ENDPOINTS.USUARIOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.USUARIOS}/${id}`),
};
