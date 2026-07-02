import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Categoria {
  id: number;
  nombre: string;
  nivel: string | null;
  descripcion: string | null;
  id_categoria_padre: number | null;
}

export interface CategoriaCreate {
  nombre: string;
  nivel?: string;
  descripcion?: string;
  id_categoria_padre?: number | null;
}

export interface CategoriaUpdate {
  nombre?: string;
  nivel?: string;
  descripcion?: string;
  id_categoria_padre?: number | null;
}

export const categoriasApi = {
  listar: (params?: PageParams) => api.get<Page<Categoria>>(ENDPOINTS.CATEGORIAS, { params }),
  listarTodos: () => fetchAllPages<Categoria>((p) => api.get<Page<Categoria>>(ENDPOINTS.CATEGORIAS, { params: p })),
  obtener: (id: number) => api.get<Categoria>(`${ENDPOINTS.CATEGORIAS}/${id}`),
  crear: (data: CategoriaCreate) => api.post<Categoria>(ENDPOINTS.CATEGORIAS, data),
  actualizar: (id: number, data: CategoriaUpdate) =>
    api.patch<Categoria>(`${ENDPOINTS.CATEGORIAS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CATEGORIAS}/${id}`),
};
