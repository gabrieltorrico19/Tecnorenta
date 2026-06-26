import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface ChecklistEstado {
  id: number;
  id_asignacion: number;
  momento: string;
  pantalla: string;
  teclado: string;
  carcasa: string;
  cargador: boolean;
  observaciones: string | null;
  url_fotos: string | null;
  id_usuario: number;
  fecha_registro: string | null;
}

export interface ChecklistEstadoCreate {
  id_asignacion: number;
  momento: string;
  pantalla: string;
  teclado: string;
  carcasa: string;
  cargador: boolean;
  observaciones?: string;
  url_fotos?: string;
  id_usuario: number;
}

export interface ChecklistEstadoUpdate {
  momento?: string;
  pantalla?: string;
  teclado?: string;
  carcasa?: string;
  cargador?: boolean;
  observaciones?: string;
  url_fotos?: string;
}

export const checklistEstadoApi = {
  listarPorAsignacion: (asignacionId: number) =>
    api.get<ChecklistEstado[]>(`${ENDPOINTS.CHECKLIST_ESTADO}/asignacion/${asignacionId}`),
  obtener: (id: number) => api.get<ChecklistEstado>(`${ENDPOINTS.CHECKLIST_ESTADO}/${id}`),
  crear: (data: ChecklistEstadoCreate) => api.post<ChecklistEstado>(ENDPOINTS.CHECKLIST_ESTADO, data),
  actualizar: (id: number, data: ChecklistEstadoUpdate) =>
    api.patch<ChecklistEstado>(`${ENDPOINTS.CHECKLIST_ESTADO}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.CHECKLIST_ESTADO}/${id}`),
};
