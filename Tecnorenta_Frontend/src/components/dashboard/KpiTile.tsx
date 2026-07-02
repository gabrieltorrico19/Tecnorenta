import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { KpiCard, Semaforo } from "../../api/dashboard.api";
import { formatCurrency, formatNumber, formatPercent, formatDelta } from "../../utils/helpers";

const semColor: Record<Semaforo, string> = {
  verde: "var(--success)",
  ambar: "var(--warning)",
  rojo: "var(--danger)",
  info: "var(--accent)",
};

function formatValor(valor: number, unidad: KpiCard["unidad"]): string {
  switch (unidad) {
    case "moneda":
      return formatCurrency(valor);
    case "porcentaje":
      return formatPercent(valor);
    case "anios":
      return `${formatNumber(valor, 1)} años`;
    default:
      return formatNumber(valor);
  }
}

function formatMeta(meta: number | null, unidad: KpiCard["unidad"]): string | null {
  if (meta === null || meta === undefined) return null;
  return `Meta: ${formatValor(meta, unidad)}`;
}

/** Devuelve true si la variación es favorable para el negocio. */
function tendenciaEsBuena(delta: number, mejorArriba: boolean): boolean {
  if (delta === 0) return true;
  return mejorArriba ? delta > 0 : delta < 0;
}

export default function KpiTile({ kpi }: { kpi: KpiCard }) {
  const color = semColor[kpi.semaforo] ?? "var(--accent)";
  const meta = formatMeta(kpi.meta, kpi.unidad);

  const tieneTendencia = kpi.tendencia_pct !== null && kpi.tendencia_pct !== undefined;
  const delta = kpi.tendencia_pct ?? 0;
  const buena = tendenciaEsBuena(delta, kpi.mejor_arriba);
  const TrendIcon = delta > 0 ? TrendingUp : delta < 0 ? TrendingDown : Minus;

  return (
    <div style={{ ...styles.tile, borderLeft: `4px solid ${color}` }} title={kpi.decision}>
      <div style={styles.headerRow}>
        <span style={styles.nombre}>{kpi.nombre}</span>
        <span style={{ ...styles.dot, background: color }} />
      </div>
      <div style={styles.valorRow}>
        <span style={{ ...styles.valor, color }}>{formatValor(kpi.valor, kpi.unidad)}</span>
        {tieneTendencia && (
          <span style={{ ...styles.trend, color: buena ? "var(--success)" : "var(--danger)" }}>
            <TrendIcon size={14} />
            {formatDelta(delta)}
          </span>
        )}
      </div>
      <div style={styles.footerRow}>
        {meta && <span style={styles.meta}>{meta}</span>}
        <span style={styles.categoria}>{kpi.categoria}</span>
      </div>
      {kpi.descripcion && <p style={styles.desc}>{kpi.descripcion}</p>}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  tile: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    padding: "var(--space-md)",
    display: "flex",
    flexDirection: "column",
    gap: "var(--space-xs)",
    minHeight: 118,
  },
  headerRow: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: "var(--space-sm)" },
  nombre: { fontSize: "var(--font-size-sm)", color: "var(--text-secondary)", fontWeight: 600, lineHeight: 1.2 },
  dot: { width: 8, height: 8, borderRadius: "50%", flexShrink: 0 },
  valorRow: { display: "flex", alignItems: "baseline", gap: "var(--space-sm)", flexWrap: "wrap" },
  valor: { fontSize: "1.6rem", fontWeight: 700, lineHeight: 1.1 },
  trend: { display: "inline-flex", alignItems: "center", gap: 2, fontSize: "var(--font-size-sm)", fontWeight: 600 },
  footerRow: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: "var(--space-sm)" },
  meta: { fontSize: "var(--font-size-sm)", color: "var(--text-muted)" },
  categoria: { fontSize: "0.7rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.04em" },
  desc: { fontSize: "0.72rem", color: "var(--text-muted)", margin: 0, lineHeight: 1.35 },
};
