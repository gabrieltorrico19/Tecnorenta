import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, Legend, CartesianGrid,
} from "recharts";
import { AlertTriangle, ArrowRight, UserPlus, Building2, Monitor, FileText } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import KpiTile from "../components/dashboard/KpiTile";
import { dashboardApi } from "../api/dashboard.api";
import type {
  DashboardStats, KpisResponse, Recomendacion, TendenciasResponse, ContratoProximoVencer,
} from "../api/dashboard.api";
import { formatCurrency, formatDate } from "../utils/helpers";

const chartColors: Record<string, string> = {
  disponible: "#22c55e", rentado: "#3b82f6", mantenimiento: "#f59e0b", baja: "#ef4444",
  activo: "#22c55e", vencido: "#ef4444", cancelado: "#6b6b6b", renovado: "#3b82f6",
  pagado: "#22c55e", pendiente: "#f59e0b",
  leve: "#22c55e", moderado: "#f59e0b", grave: "#ef4444",
  preventivo: "#22c55e", correctivo: "#ef4444",
};

const sevVariant: Record<string, "danger" | "warning" | "info"> = {
  alta: "danger", media: "warning", baja: "info",
};
const sevColor: Record<string, string> = {
  alta: "var(--danger)", media: "var(--warning)", baja: "var(--accent)",
};

function toData(rec: Record<string, number>): { name: string; value: number }[] {
  return Object.entries(rec).map(([name, value]) => ({ name, value }));
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [kpis, setKpis] = useState<KpisResponse | null>(null);
  const [recs, setRecs] = useState<Recomendacion[]>([]);
  const [tend, setTend] = useState<TendenciasResponse | null>(null);
  const [proximos, setProximos] = useState<ContratoProximoVencer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([
      dashboardApi.stats(),
      dashboardApi.kpis(),
      dashboardApi.recomendaciones(),
      dashboardApi.tendencias(6),
      dashboardApi.contratosProximosVencer(30),
    ])
      .then(([s, k, r, t, pv]) => {
        setStats(s.data);
        setKpis(k.data);
        setRecs(r.data);
        setTend(t.data);
        setProximos(pv.data.filter((c) => c.dias_restantes >= 0 && c.dias_restantes <= 30));
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div style={styles.page}>
        <h1 style={styles.pageTitle}>Panel de decisión</h1>
        <p style={styles.emptyText}>Cargando indicadores...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.page}>
        <h1 style={styles.pageTitle}>Panel de decisión</h1>
        <div style={{ ...styles.alertBanner, background: "#450a0a", border: "1px solid var(--danger)", color: "var(--danger)" }}>
          <AlertTriangle size={20} />
          <span>No se pudo cargar el panel. Revisa tu conexión con el servidor e inténtalo de nuevo.</span>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <div style={styles.headerRow}>
        <div>
          <h1 style={styles.pageTitle}>Panel de decisión</h1>
          {user && <p style={styles.welcome}>Bienvenido, {user.nombre || user.email}</p>}
        </div>
        {kpis && <span style={styles.generado}>Actualizado: {formatDate(kpis.generado)}</span>}
      </div>

      {proximos.length > 0 && (
        <div style={styles.alertBanner}>
          <AlertTriangle size={20} />
          <span style={{ flex: 1 }}>
            {proximos.length} contrato(s) vencen en 30 días · Ingreso en riesgo{" "}
            {formatCurrency(stats?.ingreso_en_riesgo_vencimientos ?? 0)}
          </span>
          <Button variant="secondary" onClick={() => navigate("/contratos")}>Ver contratos</Button>
        </div>
      )}

      {/* ---------------- FRANJA 1: SALUD DEL NEGOCIO ---------------- */}
      <Franja title="Salud del negocio" subtitle="Indicadores financieros y estratégicos">
        <div style={styles.kpiGrid}>
          {kpis?.salud.map((k) => <KpiTile key={k.clave} kpi={k} />)}
        </div>
      </Franja>

      {/* ---------------- FRANJA 2: OPERACIÓN Y RIESGOS ---------------- */}
      <Franja title="Operación y riesgos" subtitle="Distribuciones, mantenimiento e incidencias">
        <div style={styles.kpiGrid}>
          {kpis?.operacion.map((k) => <KpiTile key={k.clave} kpi={k} />)}
        </div>

        <div style={styles.chartGrid}>
          <Card title="Evolución del ingreso (MRR vs. cobrado)" style={styles.chartCard}>
            {!tend || tend.serie.length === 0 ? (
              <p style={styles.emptyText}>Sin datos de tendencia</p>
            ) : (
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={tend.serie}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="periodo" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <YAxis tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: "var(--text-primary)" }} />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                  <Line type="monotone" dataKey="mrr" name="MRR" stroke="#3b82f6" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="cobrado" name="Cobrado" stroke="#22c55e" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </Card>

          <Card title="Activos por estado" style={styles.chartCard}>
            <PieChartBlock data={toData(stats?.activos_por_estado ?? {})} />
          </Card>

          <Card title="Contratos por estado" style={styles.chartCard}>
            <BarChartBlock data={toData(stats?.contratos_por_estado ?? {})} />
          </Card>

          <Card title="Pagos por estado" style={styles.chartCard}>
            <PieChartBlock data={toData(stats?.pagos_por_estado ?? {})} />
          </Card>

          <Card title="Incidencias abiertas por gravedad" style={styles.chartCard}>
            <BarChartBlock data={toData(stats?.incidencias_por_gravedad ?? {})} />
          </Card>

          <Card title="Costo de mantenimiento (preventivo vs. correctivo)" style={styles.chartCard}>
            {!stats || stats.costo_mantenimiento_total === 0 ? (
              <p style={styles.emptyText}>Sin mantenimientos registrados</p>
            ) : (
              <PieChartBlock
                data={[
                  { name: "preventivo", value: stats.costo_mantenimiento_preventivo },
                  { name: "correctivo", value: stats.costo_mantenimiento_correctivo },
                ]}
                money
              />
            )}
          </Card>
        </div>
      </Franja>

      {/* ---------------- FRANJA 3: DECISIONES RECOMENDADAS ---------------- */}
      <Franja title="Decisiones recomendadas" subtitle="Acciones sugeridas según los KPIs de hoy">
        <div style={styles.recGrid}>
          {recs.map((r) => (
            <div key={r.id} style={{ ...styles.recCard, borderLeft: `4px solid ${sevColor[r.severidad]}` }}>
              <div style={styles.recHeader}>
                <Badge variant={sevVariant[r.severidad] ?? "info"}>{r.severidad.toUpperCase()}</Badge>
                <span style={styles.recTitulo}>{r.titulo}</span>
              </div>
              <p style={styles.recDetalle}>{r.detalle}</p>
              <p style={styles.recAccion}>→ {r.accion}</p>
              {r.ruta && (
                <Button
                  variant="secondary"
                  icon={<ArrowRight size={14} />}
                  onClick={() => navigate(r.ruta as string)}
                  style={{ alignSelf: "flex-start" }}
                >
                  Actuar
                </Button>
              )}
            </div>
          ))}
        </div>
      </Franja>

      {/* ---------------- ACCESO RÁPIDO ---------------- */}
      <Card title="Acceso rápido" style={{ marginTop: "var(--space-md)" }}>
        <div style={styles.quickAccessGrid}>
          <Button variant="secondary" icon={<UserPlus size={16} />} onClick={() => navigate("/usuarios/nuevo")}>Usuario</Button>
          <Button variant="secondary" icon={<Building2 size={16} />} onClick={() => navigate("/clientes/nuevo")}>Cliente</Button>
          <Button variant="secondary" icon={<Monitor size={16} />} onClick={() => navigate("/activos/nuevo")}>Activo</Button>
          <Button variant="secondary" icon={<FileText size={16} />} onClick={() => navigate("/contratos/nuevo")}>Contrato</Button>
        </div>
      </Card>
    </div>
  );
}

/* ------------------------- subcomponentes ------------------------- */

function Franja({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) {
  return (
    <section style={styles.franja}>
      <div style={styles.franjaHead}>
        <h2 style={styles.franjaTitle}>{title}</h2>
        <span style={styles.franjaSub}>{subtitle}</span>
      </div>
      {children}
    </section>
  );
}

function PieChartBlock({ data, money }: { data: { name: string; value: number }[]; money?: boolean }) {
  const filtered = data.filter((d) => d.value > 0);
  if (filtered.length === 0) return <p style={styles.emptyText}>Sin datos</p>;
  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie
          data={filtered}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={72}
          label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}
        >
          {filtered.map((d) => <Cell key={d.name} fill={chartColors[d.name] || "#666"} />)}
        </Pie>
        <Tooltip
          contentStyle={tooltipStyle}
          formatter={(value) => (money ? formatCurrency(Number(value)) : String(value))}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}

function BarChartBlock({ data }: { data: { name: string; value: number }[] }) {
  if (data.length === 0) return <p style={styles.emptyText}>Sin datos</p>;
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data}>
        <XAxis dataKey="name" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
        <YAxis allowDecimals={false} tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
        <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: "var(--text-primary)" }} cursor={{ fill: "var(--bg-tertiary)" }} />
        <Bar dataKey="value" radius={[4, 4, 0, 0]}>
          {data.map((d) => <Cell key={d.name} fill={chartColors[d.name] || "#666"} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

const tooltipStyle: React.CSSProperties = {
  background: "var(--bg-secondary)",
  border: "1px solid var(--border)",
  borderRadius: 4,
};

const styles: Record<string, React.CSSProperties> = {
  page: { padding: "var(--space-lg)", background: "var(--bg-primary)", minHeight: "100vh", color: "var(--text-primary)" },
  headerRow: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--space-sm)", marginBottom: "var(--space-md)" },
  pageTitle: { fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-xs)" },
  welcome: { color: "var(--text-secondary)", fontSize: "var(--font-size-md)" },
  generado: { color: "var(--text-muted)", fontSize: "var(--font-size-sm)" },
  alertBanner: {
    display: "flex", alignItems: "center", gap: "var(--space-sm)",
    padding: "var(--space-sm) var(--space-md)", background: "#451a03",
    border: "1px solid var(--warning)", borderRadius: "var(--radius-sm)",
    color: "var(--warning)", marginBottom: "var(--space-md)",
  },
  franja: { marginBottom: "var(--space-lg)" },
  franjaHead: { display: "flex", alignItems: "baseline", gap: "var(--space-sm)", marginBottom: "var(--space-sm)", borderBottom: "1px solid var(--border)", paddingBottom: "var(--space-xs)", flexWrap: "wrap" },
  franjaTitle: { fontSize: "var(--font-size-lg)", fontWeight: 700 },
  franjaSub: { fontSize: "var(--font-size-sm)", color: "var(--text-muted)" },
  kpiGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(230px, 1fr))", gap: "var(--space-md)", marginBottom: "var(--space-md)" },
  chartGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(330px, 1fr))", gap: "var(--space-md)" },
  chartCard: { minHeight: 280 },
  recGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "var(--space-md)" },
  recCard: {
    background: "var(--bg-secondary)", border: "1px solid var(--border)", borderRadius: "var(--radius)",
    padding: "var(--space-md)", display: "flex", flexDirection: "column", gap: "var(--space-xs)",
  },
  recHeader: { display: "flex", alignItems: "center", gap: "var(--space-sm)" },
  recTitulo: { fontWeight: 600, fontSize: "var(--font-size-md)" },
  recDetalle: { color: "var(--text-secondary)", fontSize: "var(--font-size-sm)", margin: 0, lineHeight: 1.4 },
  recAccion: { color: "var(--text-primary)", fontSize: "var(--font-size-sm)", fontWeight: 500, margin: "var(--space-xs) 0" },
  quickAccessGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "var(--space-sm)" },
  emptyText: { color: "var(--text-muted)", fontSize: "var(--font-size-md)", textAlign: "center", padding: "var(--space-lg) 0" },
};
