import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export type UnidadInforme = "texto" | "numero" | "moneda" | "porcentaje" | "fecha" | "badge";

export interface OpcionFiltro {
  value: string;
  label: string;
}

export interface FiltroInforme {
  key: string;
  label: string;
  tipo: "select" | "date";
  opciones: OpcionFiltro[];
}

export interface TipoInforme {
  tipo: string;
  nombre: string;
  descripcion: string;
  filtros: FiltroInforme[];
}

export interface ResumenItem {
  etiqueta: string;
  valor: string | number;
  unidad: UnidadInforme;
}

export interface ColumnaInforme {
  key: string;
  label: string;
  unidad: UnidadInforme;
}

export interface Informe {
  tipo: string;
  titulo: string;
  generado: string;
  filtros_aplicados: Record<string, string>;
  resumen: ResumenItem[];
  columnas: ColumnaInforme[];
  filas: Record<string, unknown>[];
  total_filas: number;
}

/** Elimina claves vacías para no ensuciar la query string. */
function limpiar(filtros: Record<string, string>): Record<string, string> {
  return Object.fromEntries(Object.entries(filtros).filter(([, v]) => v !== "" && v != null));
}

export const informesApi = {
  tipos: () => api.get<TipoInforme[]>(`${ENDPOINTS.INFORMES}/tipos`),
  generar: (tipo: string, filtros: Record<string, string> = {}) =>
    api.get<Informe>(`${ENDPOINTS.INFORMES}/${tipo}`, { params: limpiar(filtros) }),
  csvUrl: (tipo: string, filtros: Record<string, string> = {}) => {
    const qs = new URLSearchParams(limpiar(filtros)).toString();
    return `${ENDPOINTS.INFORMES}/${tipo}/csv${qs ? `?${qs}` : ""}`;
  },
};
