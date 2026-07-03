import { useCallback, useEffect, useMemo, useState } from "react";
import {
  informesApi,
  type TipoInforme,
  type Informe,
  type ColumnaInforme,
  type UnidadInforme,
} from "../../api/informes.api";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Badge from "../../components/common/Badge";
import FilterBar from "../../components/common/FilterBar";
import { formatCurrency, formatNumber, formatPercent, formatDate } from "../../utils/helpers";
import { FileBarChart, Download, RefreshCw } from "lucide-react";

const badgeVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  disponible: "success", rentado: "info", mantenimiento: "warning", baja: "danger",
  activo: "success", vencido: "danger", cancelado: "danger", renovado: "info",
  pagado: "success", pendiente: "warning",
  preventivo: "info", correctivo: "warning",
  leve: "info", moderado: "warning", grave: "danger",
  abierto: "danger", en_atencion: "warning", cerrado: "success",
};

function formatCell(value: unknown, unidad: UnidadInforme): React.ReactNode {
  if (value === null || value === undefined || value === "") return "—";
  switch (unidad) {
    case "moneda":
      return formatCurrency(Number(value), 2);
    case "porcentaje":
      return formatPercent(Number(value));
    case "numero":
      return formatNumber(Number(value));
    case "fecha":
      return formatDate(String(value));
    case "badge": {
      const key = String(value);
      return <Badge variant={badgeVariant[key] || "default"}>{key.replace(/_/g, " ")}</Badge>;
    }
    default:
      return String(value);
  }
}

export default function Informes() {
  const [tipos, setTipos] = useState<TipoInforme[]>([]);
  const [tipoActivo, setTipoActivo] = useState<string>("");
  const [filtros, setFiltros] = useState<Record<string, string>>({});
  const [informe, setInforme] = useState<Informe | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const tipoActual = useMemo(() => tipos.find((t) => t.tipo === tipoActivo), [tipos, tipoActivo]);

  useEffect(() => {
    informesApi.tipos()
      .then((res) => {
        setTipos(res.data);
        if (res.data.length) setTipoActivo(res.data[0].tipo);
      })
      .catch(() => setError("No se pudo cargar el catálogo de informes"));
  }, []);

  const generar = useCallback(async (tipo: string, f: Record<string, string>) => {
    if (!tipo) return;
    setLoading(true);
    setError(null);
    try {
      const res = await informesApi.generar(tipo, f);
      setInforme(res.data);
    } catch {
      setError("No se pudo generar el informe");
      setInforme(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // Al cambiar de tipo: limpia filtros y genera el informe base.
  useEffect(() => {
    if (!tipoActivo) return;
    setFiltros({});
    generar(tipoActivo, {});
  }, [tipoActivo, generar]);

  const hayFiltros = Object.values(filtros).some((v) => v !== "");

  const csvHref = tipoActivo ? informesApi.csvUrl(tipoActivo, filtros) : "#";

  return (
    <div>
      <div style={headerStyle}>
        <h2 style={{ display: "flex", alignItems: "center", gap: "var(--space-sm)" }}>
          <FileBarChart size={22} /> Informes
        </h2>
        {informe && (
          <a href={csvHref} style={{ textDecoration: "none" }}>
            <Button variant="secondary" icon={<Download size={16} />}>Exportar CSV</Button>
          </a>
        )}
      </div>

      {/* Selector de tipo de informe */}
      <div style={tabsStyle}>
        {tipos.map((t) => (
          <button
            key={t.tipo}
            onClick={() => setTipoActivo(t.tipo)}
            style={{
              ...tabStyle,
              background: t.tipo === tipoActivo ? "var(--accent)" : "var(--bg-tertiary)",
              color: t.tipo === tipoActivo ? "#fff" : "var(--text-secondary)",
            }}
            title={t.descripcion}
          >
            {t.nombre}
          </button>
        ))}
      </div>

      {tipoActual && (
        <p style={descStyle}>{tipoActual.descripcion}</p>
      )}

      {/* Filtros dinámicos del informe seleccionado */}
      {tipoActual && tipoActual.filtros.length > 0 && (
        <FilterBar hayFiltros={hayFiltros} onLimpiar={() => { setFiltros({}); generar(tipoActivo, {}); }}>
          {tipoActual.filtros.map((f) => (
            f.tipo === "select" ? (
              <select
                key={f.key}
                value={filtros[f.key] ?? ""}
                onChange={(e) => setFiltros((prev) => ({ ...prev, [f.key]: e.target.value }))}
              >
                <option value="">{f.label}: todos</option>
                {f.opciones.map((o) => (<option key={o.value} value={o.value}>{o.label}</option>))}
              </select>
            ) : (
              <label key={f.key} style={dateLabelStyle}>
                <span style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>{f.label}</span>
                <input
                  type="date"
                  value={filtros[f.key] ?? ""}
                  onChange={(e) => setFiltros((prev) => ({ ...prev, [f.key]: e.target.value }))}
                />
              </label>
            )
          ))}
          <Button icon={<RefreshCw size={14} />} onClick={() => generar(tipoActivo, filtros)}>
            Aplicar
          </Button>
        </FilterBar>
      )}

      {error && <div style={errorStyle}>{error}</div>}

      {/* Resumen (tarjetas tipo KPI) */}
      {informe && informe.resumen.length > 0 && (
        <div style={resumenGrid}>
          {informe.resumen.map((r) => (
            <Card key={r.etiqueta}>
              <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", marginBottom: 4 }}>{r.etiqueta}</div>
              <div style={{ fontSize: "1.5rem", fontWeight: 700, color: "var(--text-primary)" }}>
                {formatCell(r.valor, r.unidad)}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Tabla del informe */}
      {loading ? (
        <p style={mutedStyle}>Generando informe…</p>
      ) : informe ? (
        <>
          <div style={{ overflowX: "auto", marginTop: "var(--space-md)" }}>
            <table>
              <thead>
                <tr>{informe.columnas.map((c: ColumnaInforme) => <th key={c.key}>{c.label}</th>)}</tr>
              </thead>
              <tbody>
                {informe.filas.length === 0 ? (
                  <tr><td colSpan={informe.columnas.length} style={{ textAlign: "center", color: "var(--text-muted)" }}>Sin registros para los filtros seleccionados</td></tr>
                ) : (
                  informe.filas.map((fila, i) => (
                    <tr key={i}>
                      {informe.columnas.map((c) => (
                        <td key={c.key}>{formatCell(fila[c.key], c.unidad)}</td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          {informe.total_filas > informe.filas.length && (
            <p style={mutedStyle}>
              Mostrando {informe.filas.length} de {informe.total_filas} filas. Exporte a CSV para el detalle completo.
            </p>
          )}
        </>
      ) : null}
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-md)",
};
const tabsStyle: React.CSSProperties = {
  display: "flex", flexWrap: "wrap", gap: "var(--space-sm)", marginBottom: "var(--space-sm)",
};
const tabStyle: React.CSSProperties = {
  border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "0.4rem 0.9rem",
  cursor: "pointer", fontWeight: 600, fontSize: "0.85rem",
};
const descStyle: React.CSSProperties = {
  color: "var(--text-muted)", fontSize: "0.85rem", marginBottom: "var(--space-md)",
};
const dateLabelStyle: React.CSSProperties = { display: "flex", flexDirection: "column", gap: 2 };
const resumenGrid: React.CSSProperties = {
  display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: "var(--space-md)", marginTop: "var(--space-sm)",
};
const mutedStyle: React.CSSProperties = { color: "var(--text-muted)", padding: "var(--space-md) 0", textAlign: "center" };
const errorStyle: React.CSSProperties = { color: "var(--danger)", padding: "var(--space-md)", textAlign: "center" };
