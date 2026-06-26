import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import { useToast } from "../../context/ToastContext";
import { rolesApi, type Rol } from "../../api/roles.api";
import { formatDate } from "../../utils/helpers";
import { Plus } from "lucide-react";

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

  useEffect(() => { listar(); }, [listar]);

  return { roles, loading, error, listar };
}

const columns = [
  { key: "id", label: "ID" },
  { key: "nombre", label: "Nombre" },
  { key: "descripcion", label: "Descripción" },
  { key: "activo", label: "Activo", render: (row: Rol) => row.activo ? <Badge variant="success">Activo</Badge> : <Badge variant="danger">Inactivo</Badge> },
  { key: "created_at", label: "Creado", render: (row: Rol) => formatDate(row.created_at) },
];

export default function ListaRoles() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { roles, loading, error, listar } = useRoles();
  const [deleteTarget, setDeleteTarget] = useState<Rol | null>(null);

  const eliminar = async () => {
    if (!deleteTarget) return;
    try {
      await rolesApi.eliminar(deleteTarget.id);
      toast("Rol eliminado correctamente", "success");
      listar();
    } catch {
      toast("Error al eliminar el rol", "error");
    }
    setDeleteTarget(null);
  };

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Roles</h2>
        <Button onClick={() => navigate("/roles/nuevo")} icon={<Plus size={16} />}>Nuevo Rol</Button>
      </div>
      <DataTable columns={columns} data={roles} loading={loading} error={error}
        onEdit={(row) => navigate(`/roles/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar rol"
        message={`¿Está seguro de eliminar el rol "${deleteTarget?.nombre}"?`}
        onConfirm={eliminar}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}

const topBar: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
