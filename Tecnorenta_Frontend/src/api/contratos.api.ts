import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Contrato {
  id: number;
  id_cliente: number;
  fecha_inicio: string;
  fecha_fin: string;
  condiciones_uso: string | null;
  estado: string;
  monto_mensual: number;
  url_documento: string | null;
}

export interface ContratoCreate {
  id_cliente: number;
  fecha_inicio: string;
  fecha_fin: string;
  condiciones_uso?: string;
  estado: string;
  monto_mensual: number;
}

export interface ContratoUpdate {
  fecha_inicio?: string;
  fecha_fin?: string;
  condiciones_uso?: string;
  estado?: string;
  monto_mensual?: number;
  id_cliente?: number;
  url_documento?: string;
}

export const contratosApi = {
  listar: () => api.get<Contrato[]>(ENDPOINTS.CONTRATOS),
  obtener: (id: number) => api.get<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`),
  crear: (data: ContratoCreate) => api.post<Contrato>(ENDPOINTS.CONTRATOS, data),
  actualizar: (id: number, data: ContratoUpdate) =>
    api.patch<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CONTRATOS}/${id}`),
};
