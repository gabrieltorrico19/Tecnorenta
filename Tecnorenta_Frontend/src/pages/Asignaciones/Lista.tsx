import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { asignacionesApi, type Asignacion } from "../../api/asignaciones.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  Activa: "success",
  Pendiente: "warning",
  Devuelto: "info",
  Cancelada: "danger",
};

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-MX", { year: "numeric", month: "2-digit", day: "2-digit" });
}

export default function ListaAsignaciones() {
  const navigate = useNavigate();
  const [asignaciones, setAsignaciones] = useState<Asignacion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await asignacionesApi.listar();
      setAsignaciones(res.data);
    } catch {
      setError("Error al cargar asignaciones");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = async (asignacion: Asignacion) => {
    if (!window.confirm(`¿Eliminar asignación #${asignacion.id}?`)) return;
    try {
      await asignacionesApi.eliminar(asignacion.id);
      listar();
    } catch {
      alert("Error al eliminar asignación");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "activo_nombre",
      label: "Activo",
      render: (row: Asignacion) => <>{row.activo_nombre || "—"}</>,
    },
    {
      key: "usuario_nombre",
      label: "Usuario",
      render: (row: Asignacion) => <>{row.usuario_nombre || "—"}</>,
    },
    {
      key: "fecha_asignacion",
      label: "Fecha Asignación",
      render: (row: Asignacion) => <>{formatDate(row.fecha_asignacion)}</>,
    },
    {
      key: "fecha_devolucion",
      label: "Fecha Devolución",
      render: (row: Asignacion) => <>{formatDate(row.fecha_devolucion)}</>,
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Asignacion) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Asignaciones</h2>
        <button onClick={() => navigate("/asignaciones/nuevo")} style={btnPrimary}>
          + Nueva Asignación
        </button>
      </div>
      <DataTable
        columns={columns}
        data={asignaciones}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/asignaciones/editar/${row.id}`)}
        onDelete={eliminar}
      />
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "1rem",
};

const btnPrimary: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.5rem 1rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.85rem",
};
