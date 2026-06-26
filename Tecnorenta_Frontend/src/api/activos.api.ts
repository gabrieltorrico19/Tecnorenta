import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface Activo {
  id: number;
  codigo: string;
  nombre: string;
  descripcion: string | null;
  categoria_id: number;
  categoria_nombre?: string;
  estado: string;
  numero_serie: string | null;
  valor_adquisicion: number | null;
  fecha_adquisicion: string | null;
  ubicacion_actual: string | null;
  latitud: number | null;
  longitud: number | null;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface ActivoCreate {
  codigo: string;
  nombre: string;
  descripcion?: string;
  categoria_id: number;
  estado: string;
  numero_serie?: string;
  valor_adquisicion?: number;
  fecha_adquisicion?: string;
  ubicacion_actual?: string;
  latitud?: number | null;
  longitud?: number | null;
}

export interface ActivoUpdate {
  nombre?: string;
  descripcion?: string;
  categoria_id?: number;
  estado?: string;
  numero_serie?: string;
  valor_adquisicion?: number;
  fecha_adquisicion?: string;
  ubicacion_actual?: string;
  latitud?: number | null;
  longitud?: number | null;
  activo?: boolean;
}

export interface ActivoFoto {
  id: number;
  id_activo: number;
  url: string;
  orden: number;
  fecha_subida: string | null;
}

export const activosApi = {
  listar: () => api.get<Activo[]>(ENDPOINTS.ACTIVOS),
  obtener: (id: number) => api.get<Activo>(`${ENDPOINTS.ACTIVOS}/${id}`),
  crear: (data: ActivoCreate) => api.post<Activo>(ENDPOINTS.ACTIVOS, data),
  actualizar: (id: number, data: ActivoUpdate) =>
    api.patch<Activo>(`${ENDPOINTS.ACTIVOS}/${id}`, data),
  eliminar: (id: number) => api.delete(`${ENDPOINTS.ACTIVOS}/${id}`),
  listarFotos: (activoId: number) => api.get<ActivoFoto[]>(`${ENDPOINTS.ACTIVOS}/${activoId}/fotos`),
  subirFoto: (activoId: number, file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return api.post<ActivoFoto>(`${ENDPOINTS.ACTIVOS}/${activoId}/fotos`, fd);
  },
  eliminarFoto: (activoId: number, fotoId: number) =>
    api.delete(`${ENDPOINTS.ACTIVOS}/${activoId}/fotos/${fotoId}`),
};
