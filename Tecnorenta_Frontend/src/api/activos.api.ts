import api from "./axios";
import { ENDPOINTS } from "./endpoints";
import { fetchAllPages, type Page, type PageParams } from "./pagination";

export interface Activo {
  id: number;
  codigo_inventario: string;
  modelo: string;
  numero_serie: string;
  estado: string;
  fecha_compra: string | null;
  valor_depreciado: number;
  id_categoria: number | null;
  categoria_nombre?: string;
  latitud: number | null;
  longitud: number | null;
  creado_por: number | null;
  fecha_creacion: string;
  modificado_por: number | null;
  fecha_modificacion: string | null;
}

export interface ActivoCreate {
  codigo_inventario: string;
  modelo: string;
  numero_serie: string;
  estado: string;
  fecha_compra?: string | null;
  valor_depreciado?: number;
  id_categoria?: number | null;
  latitud?: number | null;
  longitud?: number | null;
}

export interface ActivoUpdate {
  modelo?: string;
  numero_serie?: string;
  estado?: string;
  fecha_compra?: string | null;
  valor_depreciado?: number;
  id_categoria?: number | null;
  latitud?: number | null;
  longitud?: number | null;
}

export interface ActivoFoto {
  id: number;
  id_activo: number;
  url: string;
  orden: number;
  fecha_subida: string | null;
}

export interface ActivoFiltros extends PageParams {
  estado?: string;
  id_categoria?: number;
  q?: string;
}

export const activosApi = {
  listar: (params?: ActivoFiltros) => api.get<Page<Activo>>(ENDPOINTS.ACTIVOS, { params }),
  listarTodos: () => fetchAllPages<Activo>((p) => api.get<Page<Activo>>(ENDPOINTS.ACTIVOS, { params: p })),
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
  exportarCsv: () => `${ENDPOINTS.ACTIVOS}/exportar/formato-csv`,
};
