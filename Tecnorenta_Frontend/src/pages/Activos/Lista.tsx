import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { activosApi, type Activo } from "../../api/activos.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  Disponible: "success",
  Asignado: "warning",
  "En Mantenimiento": "warning",
  Inactivo: "danger",
  Baja: "danger",
  Reservado: "info",
};

export default function ListaActivos() {
  const navigate = useNavigate();
  const [activos, setActivos] = useState<Activo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await activosApi.listar();
      setActivos(res.data);
    } catch {
      setError("Error al cargar activos");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = async (activo: Activo) => {
    if (!window.confirm(`¿Eliminar activo "${activo.nombre}"?`)) return;
    try {
      await activosApi.eliminar(activo.id);
      listar();
    } catch {
      alert("Error al eliminar activo");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "codigo", label: "Código" },
    { key: "nombre", label: "Nombre" },
    {
      key: "categoria_nombre",
      label: "Categoría",
      render: (row: Activo) => <>{row.categoria_nombre || "—"}</>,
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Activo) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
    { key: "numero_serie", label: "Serie", render: (row: Activo) => <>{row.numero_serie || "—"}</> },
    { key: "ubicacion_actual", label: "Ubicación", render: (row: Activo) => <>{row.ubicacion_actual || "—"}</> },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Activos</h2>
        <button onClick={() => navigate("/activos/nuevo")} style={btnPrimary}>
          + Nuevo Activo
        </button>
      </div>
      <DataTable
        columns={columns}
        data={activos}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/activos/editar/${row.id}`)}
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
