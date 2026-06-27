import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useAuth } from "../context/AuthContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import { dashboardApi, type DashboardStats, type ContratoProximoVencer } from "../api/dashboard.api";
import { UserPlus, Building2, Monitor, FileText, AlertTriangle, DollarSign, Users, Package, Calendar } from "lucide-react";

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [proximosVencer, setProximosVencer] = useState<ContratoProximoVencer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      dashboardApi.stats(),
      dashboardApi.contratosProximosVencer(30),
    ]).then(([s, pv]) => {
      setStats(s.data);
      setProximosVencer(pv.data.filter((c) => c.dias_restantes <= 30 && c.dias_restantes >= 0));
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  return (
    <div style={styles.page}>
      <h1 style={styles.pageTitle}>Panel Principal</h1>
      {user && <p style={styles.welcome}>Bienvenido, {user.nombre || user.email}</p>}

      {proximosVencer.length > 0 && (
        <div style={styles.alertBanner}>
          <AlertTriangle size={20} />
          <span style={{ flex: 1 }}>{proximosVencer.length} contrato(s) próximos a vencer en los próximos 30 días</span>
          <Button variant="secondary" onClick={() => navigate("/contratos")}>Ver contratos</Button>
        </div>
      )}

      <div style={styles.grid}>
        <div style={{ ...styles.cardSpan2, ...styles.cardWrapper }}>
          <Card title="Resumen">
            {loading ? (
              <p style={styles.emptyText}>Cargando...</p>
            ) : (
              <div style={styles.statsGrid}>
                <div style={styles.statBox}>
                  <Users size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>{stats?.usuarios_count ?? 0}</span>
                  <span style={styles.statLabel}>Usuarios</span>
                </div>
                <div style={styles.statBox}>
                  <Building2 size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>{stats?.clientes_count ?? 0}</span>
                  <span style={styles.statLabel}>Clientes</span>
                </div>
                <div style={styles.statBox}>
                  <Package size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>{stats?.activos_count ?? 0}</span>
                  <span style={styles.statLabel}>Activos</span>
                </div>
                <div style={styles.statBox}>
                  <FileText size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>{stats?.contratos_count ?? 0}</span>
                  <span style={styles.statLabel}>Contratos</span>
                </div>
                <div style={styles.statBox}>
                  <DollarSign size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>${(stats?.total_ingresos_mensuales ?? 0).toLocaleString()}</span>
                  <span style={styles.statLabel}>Ingresos/mes</span>
                </div>
                <div style={styles.statBox}>
                  <Calendar size={20} style={{ color: "var(--accent)" }} />
                  <span style={styles.statNumber}>{stats?.contratos_proximos_vencer ?? 0}</span>
                  <span style={styles.statLabel}>Próximos a vencer</span>
                </div>
              </div>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Contratos por estado">
            {!stats || Object.keys(stats.contratos_por_estado).length === 0 ? (
              <p style={styles.emptyText}>Sin contratos</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={Object.entries(stats.contratos_por_estado).map(([name, value]) => ({ name, value }))}>
                  <XAxis dataKey="name" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <YAxis tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border)", borderRadius: 4 }} labelStyle={{ color: "var(--text-primary)" }} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {Object.entries(stats.contratos_por_estado).map(([estado]) => (<Cell key={estado} fill={chartColors[estado] || "#666"} />))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Activos por estado">
            {!stats || Object.keys(stats.activos_por_estado).length === 0 ? (
              <p style={styles.emptyText}>Sin activos</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={Object.entries(stats.activos_por_estado).map(([name, value]) => ({ name, value }))} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70}
                    label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}>
                    {Object.entries(stats.activos_por_estado).map(([estado]) => (<Cell key={estado} fill={chartColors[estado] || "#666"} />))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Mantenimientos pendientes">
            {!stats || stats.mantenimientos_pendientes === 0 ? (
              <p style={styles.emptyText}>Sin mantenimientos pendientes</p>
            ) : (
              <>
                <p style={styles.pendingCount}>{stats.mantenimientos_pendientes} en total</p>
              </>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Incidencias abiertas">
            {!stats || stats.incidencias_abiertas === 0 ? (
              <p style={styles.emptyText}>Sin incidencias abiertas</p>
            ) : (
              <p style={{ ...styles.pendingCount, color: "var(--danger)" }}>{stats.incidencias_abiertas} abiertas</p>
            )}
          </Card>
        </div>

        {stats && stats.pagos_vencidos > 0 && (
          <div style={styles.cardWrapper}>
            <Card title="Pagos vencidos">
              <p style={{ ...styles.pendingCount, color: "var(--danger)" }}>{stats.pagos_vencidos} pago(s) vencido(s)</p>
            </Card>
          </div>
        )}

        <div style={styles.cardWrapper}>
          <Card title="Acceso rápido">
            <div style={styles.quickAccessGrid}>
              <Button variant="secondary" icon={<UserPlus size={16} />} onClick={() => navigate("/usuarios/nuevo")}>Usuario</Button>
              <Button variant="secondary" icon={<Building2 size={16} />} onClick={() => navigate("/clientes/nuevo")}>Cliente</Button>
              <Button variant="secondary" icon={<Monitor size={16} />} onClick={() => navigate("/activos/nuevo")}>Activo</Button>
              <Button variant="secondary" icon={<FileText size={16} />} onClick={() => navigate("/contratos/nuevo")}>Contrato</Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

const chartColors: Record<string, string> = {
  disponible: "#22c55e",
  rentado: "#3b82f6",
  mantenimiento: "#f59e0b",
  baja: "#ef4444",
  activo: "#22c55e",
  vencido: "#ef4444",
  cancelado: "#6b6b6b",
};

const styles: Record<string, React.CSSProperties> = {
  page: {
    padding: "var(--space-lg)",
    background: "var(--bg-primary)",
    minHeight: "100vh",
    color: "var(--text-primary)",
  },
  pageTitle: {
    fontSize: "var(--font-size-2xl)",
    fontWeight: 700,
    marginBottom: "var(--space-xs)",
  },
  welcome: {
    color: "var(--text-secondary)",
    marginBottom: "var(--space-lg)",
    fontSize: "var(--font-size-md)",
  },
  alertBanner: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-sm)",
    padding: "var(--space-sm) var(--space-md)",
    background: "var(--warning-bg, #fef3c7)",
    border: "1px solid var(--warning-border, #f59e0b)",
    borderRadius: "var(--radius-sm)",
    color: "var(--warning-text, #92400e)",
    marginBottom: "var(--space-md)",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: "var(--space-md)",
    gridAutoRows: "auto",
  },
  cardWrapper: { gridColumn: "span 1" },
  cardSpan2: { gridColumn: "span 2" },
  statsGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: "var(--space-sm)",
  },
  statBox: {
    background: "var(--bg-tertiary)",
    borderRadius: "var(--radius-sm)",
    padding: "var(--space-md)",
    textAlign: "center",
    display: "flex",
    flexDirection: "column",
    gap: "var(--space-xs)",
    alignItems: "center",
  },
  statNumber: { fontSize: "var(--font-size-3xl)", fontWeight: 700, color: "var(--accent)" },
  statLabel: { fontSize: "var(--font-size-sm)", color: "var(--text-muted)" },
  list: { display: "flex", flexDirection: "column", gap: "var(--space-sm)" },
  listItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "var(--space-sm) 0",
    borderBottom: "1px solid var(--border)",
  },
  listItemText: { color: "var(--text-primary)", fontSize: "var(--font-size-md)", fontWeight: 500 },
  emptyText: { color: "var(--text-muted)", fontSize: "var(--font-size-md)", textAlign: "center", padding: "var(--space-md) 0" },
  pendingCount: { color: "var(--warning)", fontSize: "var(--font-size-md)", fontWeight: 600, marginBottom: "var(--space-sm)" },
  quickAccessGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-sm)" },
};
