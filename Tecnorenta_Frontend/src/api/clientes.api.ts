import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Cliente {
  id: number;
  tipo_persona: string;
  tipo_documento: string;
  numero_documento: string;
  nombre: string;
  email: string;
  telefono: string | null;
  direccion: string | null;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClienteCreate {
  tipo_persona: string;
  tipo_documento: string;
  numero_documento: string;
  nombre: string;
  email: string;
  telefono?: string;
  direccion?: string;
}

export interface ClienteUpdate {
  nombre?: string;
  email?: string;
  telefono?: string;
  direccion?: string;
  activo?: boolean;
}

export const clientesApi = {
  listar: () => api.get<Cliente[]>(ENDPOINTS.CLIENTES),
  obtener: (id: number) => api.get<Cliente>(`${ENDPOINTS.CLIENTES}/${id}`),
  crear: (data: ClienteCreate) => api.post<Cliente>(ENDPOINTS.CLIENTES, data),
  actualizar: (id: number, data: ClienteUpdate) =>
    api.patch<Cliente>(`${ENDPOINTS.CLIENTES}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CLIENTES}/${id}`),
};
