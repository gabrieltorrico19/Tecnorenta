import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import { useToast } from "../../context/ToastContext";
import { categoriasApi, type Categoria } from "../../api/categorias.api";
import { Plus } from "lucide-react";

const PAGE_SIZE = 20;

function useCategorias() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await categoriasApi.listar({ page, page_size: PAGE_SIZE });
      setCategorias(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar categorías");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => { listar(); }, [listar]);

  return { categorias, loading, error, listar, page, setPage, pages, total };
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
  const { categorias, loading, error, listar, page, setPage, pages, total } = useCategorias();
  const [deleteTarget, setDeleteTarget] = useState<Categoria | null>(null);

  const eliminar = async () => {
    if (!deleteTarget) return;
    try {
      await categoriasApi.eliminar(deleteTarget.id);
      toast("Categoría eliminada correctamente", "success");
      if (categorias.length === 1 && page > 1) setPage(page - 1);
      else listar();
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
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
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
