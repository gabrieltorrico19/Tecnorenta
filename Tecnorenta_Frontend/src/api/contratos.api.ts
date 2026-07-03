import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

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

export interface ContratoFiltros extends PageParams {
  estado?: string;
  id_cliente?: number;
}

export const contratosApi = {
  listar: (params?: ContratoFiltros) => api.get<Page<Contrato>>(ENDPOINTS.CONTRATOS, { params }),
  listarTodos: () => fetchAllPages<Contrato>((p) => api.get<Page<Contrato>>(ENDPOINTS.CONTRATOS, { params: p })),
  obtener: (id: number) => api.get<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`),
  crear: (data: ContratoCreate) => api.post<Contrato>(ENDPOINTS.CONTRATOS, data),
  actualizar: (id: number, data: ContratoUpdate) =>
    api.patch<Contrato>(`${ENDPOINTS.CONTRATOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CONTRATOS}/${id}`),
};
