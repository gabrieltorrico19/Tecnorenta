import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import { useToast } from "../../context/ToastContext";
import { historialUbicacionApi, type HistorialUbicacion } from "../../api/historial-ubicacion.api";
import { formatDate } from "../../utils/helpers";
import { Plus } from "lucide-react";

const PAGE_SIZE = 20;

function useHistorial() {
  const [registros, setRegistros] = useState<HistorialUbicacion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await historialUbicacionApi.listar({ page, page_size: PAGE_SIZE });
      setRegistros(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar historial de ubicaciones");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => { listar(); }, [listar]);

  return { registros, loading, error, listar, page, setPage, pages, total };
}

const columns = [
  { key: "id", label: "ID" },
  { key: "id_asignacion", label: "ID Asignación" },
  {
    key: "latitud",
    label: "Latitud",
    render: (row: HistorialUbicacion) => <>{row.latitud.toFixed(6)}</>,
  },
  {
    key: "longitud",
    label: "Longitud",
    render: (row: HistorialUbicacion) => <>{row.longitud.toFixed(6)}</>,
  },
  {
    key: "timestamp",
    label: "Fecha",
    render: (row: HistorialUbicacion) => <>{row.timestamp ? formatDate(row.timestamp) : "—"}</>,
  },
];

export default function ListaHistorialUbicacion() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { registros, loading, error, listar, page, setPage, pages, total } = useHistorial();
  const [deleteTarget, setDeleteTarget] = useState<HistorialUbicacion | null>(null);

  const eliminar = async () => {
    if (!deleteTarget) return;
    try {
      await historialUbicacionApi.eliminar(deleteTarget.id);
      toast("Registro de ubicación eliminado", "success");
      if (registros.length === 1 && page > 1) setPage(page - 1);
      else listar();
    } catch {
      toast("Error al eliminar el registro", "error");
    }
    setDeleteTarget(null);
  };

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Historial de Ubicaciones</h2>
        <Button onClick={() => navigate("/historial-ubicacion/nuevo")} icon={<Plus size={16} />}>
          Nuevo Registro
        </Button>
      </div>
      <DataTable
        columns={columns}
        data={registros}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/historial-ubicacion/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar registro"
        message={`¿Eliminar el registro de ubicación #${deleteTarget?.id}?`}
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
