import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import { UserPlus, Building2, Monitor, FileText } from "lucide-react";

interface Contrato { numero_contrato: string; estado: string }
interface Activo { estado: string }
interface Mantenimiento { id: number; activo_id: number; tipo_mantenimiento: string; estado: string; fecha_programada: string }
interface Incidencia { id: number; tipo_incidencia: string; estado: string; fecha_reporte: string }

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [usuariosCount, setUsuariosCount] = useState(0);
  const [clientesCount, setClientesCount] = useState(0);
  const [activos, setActivos] = useState<Activo[]>([]);
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [mantenimientos, setMantenimientos] = useState<Mantenimiento[]>([]);
  const [incidencias, setIncidencias] = useState<Incidencia[]>([]);

  useEffect(() => {
    api.get("/api/v1/usuarios").then((r) => setUsuariosCount(r.data.length)).catch(() => {});
    api.get("/api/v1/clientes").then((r) => setClientesCount(r.data.length)).catch(() => {});
    api.get("/api/v1/activos").then((r) => setActivos(r.data)).catch(() => {});
    api.get("/api/v1/contratos").then((r) => setContratos(r.data)).catch(() => {});
    api.get("/api/v1/mantenimientos").then((r) => setMantenimientos(r.data)).catch(() => {});
    api.get("/api/v1/reportes-incidencia").then((r) => setIncidencias(r.data)).catch(() => {});
  }, []);

  const activosPorEstado = activos.reduce<Record<string, number>>((acc, a) => {
    acc[a.estado] = (acc[a.estado] || 0) + 1;
    return acc;
  }, {});

  const contratosPorEstado = contratos.reduce<Record<string, number>>((acc, c) => {
    acc[c.estado] = (acc[c.estado] || 0) + 1;
    return acc;
  }, {});

  const mantenimientosPendientes = mantenimientos.filter(
    (m) => m.estado === "Pendiente" || m.estado === "En progreso"
  );

  const incidenciasRecientes = incidencias.slice(-5).reverse();

  const badgeVariant = (estado: string): "success" | "danger" | "warning" | "default" => {
    if (estado === "Activo") return "success";
    if (estado === "Inactivo" || estado === "Vencido") return "danger";
    if (estado === "Pendiente") return "warning";
    return "default";
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.pageTitle}>Panel Principal</h1>
      {user && <p style={styles.welcome}>Bienvenido, {user.nombre || user.email}</p>}

      <div style={styles.grid}>
        <div style={{ ...styles.cardSpan2, ...styles.cardWrapper }}>
          <Card title="Resumen">
            <div style={styles.statsGrid}>
              <div style={styles.statBox}>
                <span style={styles.statNumber}>{usuariosCount}</span>
                <span style={styles.statLabel}>Usuarios activos</span>
              </div>
              <div style={styles.statBox}>
                <span style={styles.statNumber}>{clientesCount}</span>
                <span style={styles.statLabel}>Clientes activos</span>
              </div>
              <div style={styles.statBox}>
                <span style={styles.statNumber}>{activos.length}</span>
                <span style={styles.statLabel}>Activos en uso</span>
              </div>
              <div style={styles.statBox}>
                <span style={styles.statNumber}>{contratos.length}</span>
                <span style={styles.statLabel}>Contratos activos</span>
              </div>
            </div>
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Contratos por estado">
            {Object.keys(contratosPorEstado).length === 0 ? (
              <p style={styles.emptyText}>Sin contratos</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={Object.entries(contratosPorEstado).map(([name, value]) => ({ name, value }))}>
                  <XAxis dataKey="name" tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <YAxis tick={{ fill: "var(--text-secondary)", fontSize: 12 }} />
                  <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border)", borderRadius: 4 }} labelStyle={{ color: "var(--text-primary)" }} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {Object.entries(contratosPorEstado).map(([estado]) => (<Cell key={estado} fill={chartColors[estado] || "#666"} />))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Activos por estado">
            {Object.keys(activosPorEstado).length === 0 ? (
              <p style={styles.emptyText}>Sin activos</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={Object.entries(activosPorEstado).map(([name, value]) => ({ name, value }))} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70}
                    label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}>
                    {Object.entries(activosPorEstado).map(([estado]) => (<Cell key={estado} fill={chartColors[estado] || "#666"} />))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Mantenimientos pendientes">
            {mantenimientosPendientes.length === 0 ? (
              <p style={styles.emptyText}>Sin mantenimientos pendientes</p>
            ) : (
              <>
                <p style={styles.pendingCount}>{mantenimientosPendientes.length} en total</p>
                <div style={styles.list}>
                  {mantenimientosPendientes.slice(0, 5).map((m) => (
                    <div key={m.id} style={styles.listItem}>
                      <span style={styles.listItemText}>{m.tipo_mantenimiento}</span>
                      <Badge variant="warning">{m.estado}</Badge>
                    </div>
                  ))}
                </div>
              </>
            )}
          </Card>
        </div>

        <div style={styles.cardWrapper}>
          <Card title="Incidencias recientes">
            {incidenciasRecientes.length === 0 ? (
              <p style={styles.emptyText}>Sin incidencias</p>
            ) : (
              <div style={styles.list}>
                {incidenciasRecientes.map((inc) => (
                  <div key={inc.id} style={styles.listItem}>
                    <span style={styles.listItemText}>{inc.tipo_incidencia}</span>
                    <Badge variant={badgeVariant(inc.estado)}>{inc.estado}</Badge>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

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
    gridTemplateColumns: "1fr 1fr",
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
