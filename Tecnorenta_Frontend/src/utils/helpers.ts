export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("es-ES", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/** Formatea un monto en bolivianos (Bs). Por defecto sin decimales. */
export function formatCurrency(value: number, decimals = 0): string {
  const n = Number.isFinite(value) ? value : 0;
  return new Intl.NumberFormat("es-BO", {
    style: "currency",
    currency: "BOB",
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(n);
}

/** Formatea un número entero/decimal con separador de miles es-BO. */
export function formatNumber(value: number, decimals = 0): string {
  const n = Number.isFinite(value) ? value : 0;
  return new Intl.NumberFormat("es-BO", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(n);
}

/** Formatea un porcentaje ya expresado en escala 0-100 (ej. 61.1 -> "61,1%"). */
export function formatPercent(value: number, decimals = 1): string {
  const n = Number.isFinite(value) ? value : 0;
  return `${formatNumber(n, decimals)}%`;
}

/** Formatea una variación con signo (+/-) para deltas de tendencia. */
export function formatDelta(value: number, decimals = 1): string {
  const n = Number.isFinite(value) ? value : 0;
  const sign = n > 0 ? "+" : "";
  return `${sign}${formatNumber(n, decimals)}%`;
}
