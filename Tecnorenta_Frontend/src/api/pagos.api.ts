import api from "./axios";
import { ENDPOINTS } from "./endpoints";

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
  listar: () => api.get<Pago[]>(ENDPOINTS.PAGOS),
  obtener: (id: number) => api.get<Pago>(`${ENDPOINTS.PAGOS}/${id}`),
  crear: (data: PagoCreate) => api.post<Pago>(ENDPOINTS.PAGOS, data),
  actualizar: (id: number, data: PagoUpdate) =>
    api.patch<Pago>(`${ENDPOINTS.PAGOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.PAGOS}/${id}`),
};
