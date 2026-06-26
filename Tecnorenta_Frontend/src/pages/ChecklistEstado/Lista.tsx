import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import Badge from "../../components/common/Badge";
import { useToast } from "../../context/ToastContext";
import { checklistEstadoApi, type ChecklistEstado } from "../../api/checklist-estado.api";
import { formatDate } from "../../utils/helpers";
import { Plus, ClipboardCheck } from "lucide-react";

const estadoComponenteVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  bien: "success",
  rayado: "warning",
  roto: "danger",
};

const momentoVariant: Record<string, "default" | "warning" | "success"> = {
  entrega: "warning",
  devolucion: "success",
};

export default function ListaChecklistEstado() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [checklists, setChecklists] = useState<ChecklistEstado[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [asignacionFilter, setAsignacionFilter] = useState("");
  const [deleteTarget, setDeleteTarget] = useState<ChecklistEstado | null>(null);

  const listar = useCallback(async (asignacionId?: number) => {
    setLoading(true);
    setError(null);
    try {
      if (asignacionId) {
        const res = await checklistEstadoApi.listarPorAsignacion(asignacionId);
        setChecklists(res.data);
      } else {
        setChecklists([]);
      }
    } catch {
      setError("Error al cargar checklists");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleFilter = () => {
    const id = asignacionFilter ? Number(asignacionFilter) : undefined;
    listar(id);
  };

  const eliminar = async () => {
    if (!deleteTarget) return;
    try {
      await checklistEstadoApi.eliminar(deleteTarget.id);
      toast("Checklist eliminado", "success");
      setChecklists((prev) => prev.filter((c) => c.id !== deleteTarget.id));
    } catch {
      toast("Error al eliminar el checklist", "error");
    }
    setDeleteTarget(null);
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "id_asignacion", label: "ID Asignación" },
    {
      key: "momento",
      label: "Momento",
      render: (row: ChecklistEstado) => (
        <Badge variant={momentoVariant[row.momento] || "default"}>{row.momento}</Badge>
      ),
    },
    {
      key: "pantalla",
      label: "Pantalla",
      render: (row: ChecklistEstado) => (
        <Badge variant={estadoComponenteVariant[row.pantalla] || "default"}>{row.pantalla}</Badge>
      ),
    },
    {
      key: "teclado",
      label: "Teclado",
      render: (row: ChecklistEstado) => (
        <Badge variant={estadoComponenteVariant[row.teclado] || "default"}>{row.teclado}</Badge>
      ),
    },
    {
      key: "carcasa",
      label: "Carcasa",
      render: (row: ChecklistEstado) => (
        <Badge variant={estadoComponenteVariant[row.carcasa] || "default"}>{row.carcasa}</Badge>
      ),
    },
    {
      key: "cargador",
      label: "Cargador",
      render: (row: ChecklistEstado) => <>{row.cargador ? "Sí" : "No"}</>,
    },
    {
      key: "fecha_registro",
      label: "Fecha",
      render: (row: ChecklistEstado) => <>{row.fecha_registro ? formatDate(row.fecha_registro) : "—"}</>,
    },
  ];

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Checklist de Estado</h2>
        <Button onClick={() => navigate("/checklist/nuevo")} icon={<Plus size={16} />}>Nuevo Checklist</Button>
      </div>
      <div style={filterBar}>
        <input
          type="number"
          placeholder="Filtrar por ID Asignación"
          value={asignacionFilter}
          onChange={(e) => setAsignacionFilter(e.target.value)}
          style={filterInput}
        />
        <Button onClick={handleFilter} icon={<ClipboardCheck size={16} />}>Buscar</Button>
      </div>
      <DataTable
        columns={columns}
        data={checklists}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/checklist/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar checklist"
        message={`¿Eliminar el checklist #${deleteTarget?.id}?`}
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

const filterBar: React.CSSProperties = {
  display: "flex",
  gap: "0.5rem",
  marginBottom: "var(--space-md)",
};

const filterInput: React.CSSProperties = {
  padding: "0.5rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "var(--font-size-md)",
  width: "200px",
};
