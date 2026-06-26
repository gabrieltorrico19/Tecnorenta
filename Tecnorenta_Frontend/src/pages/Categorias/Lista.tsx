import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import { useToast } from "../../context/ToastContext";
import { categoriasApi, type Categoria } from "../../api/categorias.api";
import { Plus } from "lucide-react";

function useCategorias() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await categoriasApi.listar();
      setCategorias(res.data);
    } catch {
      setError("Error al cargar categorías");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { listar(); }, [listar]);

  return { categorias, loading, error, listar };
}

const columns = [
  { key: "id", label: "ID" },
  { key: "nombre", label: "Nombre" },
  { key: "nivel", label: "Nivel" },
  { key: "descripcion", label: "Descripción" },
];

export default function ListaCategorias() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { categorias, loading, error, listar } = useCategorias();
  const [deleteTarget, setDeleteTarget] = useState<Categoria | null>(null);

  const eliminar = async () => {
    if (!deleteTarget) return;
    try {
      await categoriasApi.eliminar(deleteTarget.id);
      toast("Categoría eliminada correctamente", "success");
      listar();
    } catch {
      toast("Error al eliminar la categoría", "error");
    }
    setDeleteTarget(null);
  };

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Categorías</h2>
        <Button onClick={() => navigate("/categorias/nuevo")} icon={<Plus size={16} />}>Nueva Categoría</Button>
      </div>
      <DataTable columns={columns} data={categorias} loading={loading} error={error}
        onEdit={(row) => navigate(`/categorias/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar categoría"
        message={`¿Está seguro de eliminar la categoría "${deleteTarget?.nombre}"?`}
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
