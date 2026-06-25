import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import { rolesApi, type Rol } from "../../api/roles.api";
import { formatDate } from "../../utils/helpers";

function useRoles() {
  const [roles, setRoles] = useState<Rol[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await rolesApi.listar();
      setRoles(res.data);
    } catch {
      setError("Error al cargar roles");
    } finally {
      setLoading(false);
    }
  }, []);

  const eliminar = useCallback(async (id: number) => {
    if (!window.confirm("¿Está seguro de eliminar este rol?")) return;
    try {
      await rolesApi.eliminar(id);
      setRoles((prev) => prev.filter((r) => r.id !== id));
    } catch {
      alert("Error al eliminar el rol");
    }
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  return { roles, loading, error, listar, eliminar };
}

const columns = [
  { key: "id", label: "ID" },
  { key: "nombre", label: "Nombre" },
  { key: "descripcion", label: "Descripción" },
  {
    key: "activo",
    label: "Activo",
    render: (row: Rol) =>
      row.activo ? (
        <Badge variant="success">Activo</Badge>
      ) : (
        <Badge variant="danger">Inactivo</Badge>
      ),
  },
  {
    key: "created_at",
    label: "Creado",
    render: (row: Rol) => formatDate(row.created_at),
  },
];

export default function ListaRoles() {
  const navigate = useNavigate();
  const { roles, loading, error, eliminar } = useRoles();

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Roles</h2>
        <button onClick={() => navigate("/roles/nuevo")} style={btnNuevo}>
          + Nuevo Rol
        </button>
      </div>
      <DataTable
        columns={columns}
        data={roles}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/roles/editar/${row.id}`)}
        onDelete={(row) => eliminar(row.id)}
      />
    </div>
  );
}

const topBar: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "1rem",
};

const btnNuevo: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.5rem 1rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.85rem",
};
