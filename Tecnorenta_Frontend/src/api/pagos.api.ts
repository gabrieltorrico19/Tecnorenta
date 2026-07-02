import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Pago {
  id: number;
  id_contrato: number;
  concepto: string;
  monto: number;
  fecha: string;
  estado: string;
}

export interface PagoCreate {
  id_contrato: number;
  concepto: string;
  monto: number;
  fecha: string;
  estado: string;
}

export interface PagoUpdate {
  concepto?: string;
  monto?: number;
  fecha?: string;
  estado?: string;
}

export const pagosApi = {
  listar: (params?: PageParams) => api.get<Page<Pago>>(ENDPOINTS.PAGOS, { params }),
  listarTodos: () => fetchAllPages<Pago>((p) => api.get<Page<Pago>>(ENDPOINTS.PAGOS, { params: p })),
  obtener: (id: number) => api.get<Pago>(`${ENDPOINTS.PAGOS}/${id}`),
  crear: (data: PagoCreate) => api.post<Pago>(ENDPOINTS.PAGOS, data),
  actualizar: (id: number, data: PagoUpdate) =>
    api.patch<Pago>(`${ENDPOINTS.PAGOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.PAGOS}/${id}`),
};
