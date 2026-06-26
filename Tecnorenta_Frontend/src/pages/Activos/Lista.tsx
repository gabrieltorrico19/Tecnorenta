import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { activosApi, type Activo } from "../../api/activos.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import { useToast } from "../../context/ToastContext";
import { Plus } from "lucide-react";

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
  const { toast } = useToast();
  const [activos, setActivos] = useState<Activo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Activo | null>(null);

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

  useEffect(() => { listar(); }, [listar]);

  const eliminar = async (activo: Activo) => {
    try {
      await activosApi.eliminar(activo.id);
      toast("Activo eliminado correctamente", "success");
      listar();
    } catch {
      toast("Error al eliminar el activo", "error");
    }
    setDeleteTarget(null);
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "codigo", label: "Código" },
    { key: "nombre", label: "Nombre" },
    { key: "categoria_nombre", label: "Categoría", render: (row: Activo) => <>{row.categoria_nombre || "—"}</> },
    { key: "estado", label: "Estado", render: (row: Activo) => <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge> },
    { key: "numero_serie", label: "Serie", render: (row: Activo) => <>{row.numero_serie || "—"}</> },
    { key: "ubicacion_actual", label: "Ubicación", render: (row: Activo) => <>{row.ubicacion_actual || "—"}</> },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Activos</h2>
        <Button onClick={() => navigate("/activos/nuevo")} icon={<Plus size={16} />}>Nuevo Activo</Button>
      </div>
      <DataTable columns={columns} data={activos} loading={loading} error={error}
        onEdit={(row) => navigate(`/activos/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar activo"
        message={`¿Está seguro de eliminar el activo "${deleteTarget?.nombre}"?`}
        onConfirm={() => deleteTarget && eliminar(deleteTarget)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
