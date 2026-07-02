import type { AxiosResponse } from "axios";

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface PageParams {
  page?: number;
  page_size?: number;
}

/**
 * Recorre todas las páginas de un endpoint paginado y devuelve un array plano.
 * Se usa para dropdowns y mapas de búsqueda que necesitan el conjunto completo
 * (no una sola página), evitando truncar datos de forma silenciosa.
 */
export async function fetchAllPages<T>(
  fetchPage: (params: PageParams) => Promise<AxiosResponse<Page<T>>>,
  pageSize = 100
): Promise<T[]> {
  const first = await fetchPage({ page: 1, page_size: pageSize });
  const all: T[] = [...first.data.items];
  for (let p = 2; p <= first.data.pages; p++) {
    const res = await fetchPage({ page: p, page_size: pageSize });
    all.push(...res.data.items);
  }
  return all;
}
