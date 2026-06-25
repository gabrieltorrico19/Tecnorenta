import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Pago {
  id: number;
  contrato_id: number;
  contrato_numero?: string;
  monto: number;
  fecha_pago: string;
  metodo_pago: string;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface PagoCreate {
  contrato_id: number;
  monto: number;
  fecha_pago: string;
  metodo_pago: string;
  estado: string;
}

export interface PagoUpdate {
  monto?: number;
  metodo_pago?: string;
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
