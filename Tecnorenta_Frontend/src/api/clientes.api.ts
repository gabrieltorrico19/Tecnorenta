import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Cliente {
  id: number;
  razon_social: string;
  nit: string;
  direccion: string | null;
  latitud: number | null;
  longitud: number | null;
  sector: string | null;
}

export interface ClienteCreate {
  razon_social: string;
  nit: string;
  direccion?: string;
  latitud?: number | null;
  longitud?: number | null;
  sector?: string;
}

export interface ClienteUpdate {
  razon_social?: string;
  nit?: string;
  direccion?: string;
  latitud?: number | null;
  longitud?: number | null;
  sector?: string;
}

export interface ClienteFiltros extends PageParams {
  q?: string;
  sector?: string;
}

export const clientesApi = {
  listar: (params?: ClienteFiltros) => api.get<Page<Cliente>>(ENDPOINTS.CLIENTES, { params }),
  listarTodos: () => fetchAllPages<Cliente>((p) => api.get<Page<Cliente>>(ENDPOINTS.CLIENTES, { params: p })),
  obtener: (id: number) => api.get<Cliente>(`${ENDPOINTS.CLIENTES}/${id}`),
  crear: (data: ClienteCreate) => api.post<Cliente>(ENDPOINTS.CLIENTES, data),
  actualizar: (id: number, data: ClienteUpdate) =>
    api.patch<Cliente>(`${ENDPOINTS.CLIENTES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CLIENTES}/${id}`),
};
