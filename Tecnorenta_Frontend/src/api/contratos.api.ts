import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Contrato {
  id: number;
  cliente_id: number;
  cliente_nombre?: string;
  numero_contrato: string;
  fecha_inicio: string;
  fecha_fin: string;
  monto_total: number;
  estado: string;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface ContratoCreate {
  cliente_id: number;
  numero_contrato: string;
  fecha_inicio: string;
  fecha_fin: string;
  monto_total: number;
  estado: string;
}

export interface ContratoUpdate {
  fecha_fin?: string;
  monto_total?: number;
  estado?: string;
  activo?: boolean;
}

export const contratosApi = {
  listar: () => api.get<Contrato[]>(ENDPOINTS.CONTRATOS),
  obtener: (id: number) => api.get<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`),
  crear: (data: ContratoCreate) => api.post<Contrato>(ENDPOINTS.CONTRATOS, data),
  actualizar: (id: number, data: ContratoUpdate) =>
    api.patch<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CONTRATOS}/${id}`),
};
