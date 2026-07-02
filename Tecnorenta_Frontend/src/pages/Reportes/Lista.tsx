import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { reportesApi, type Reporte } from "../../api/reportes.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import { formatDate } from "../../utils/helpers";

const PAGE_SIZE = 20;

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  Reportada: "danger",
  "En Revisión": "warning",
  Resuelta: "success",
  Cerrada: "info",
};

export default function ListaReportes() {
  const navigate = useNavigate();
  const [reportes, setReportes] = useState<Reporte[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await reportesApi.listar({ page, page_size: PAGE_SIZE });
      setReportes(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar reportes");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = async (reporte: Reporte) => {
    if (!window.confirm(`¿Eliminar reporte #${reporte.id}?`)) return;
    try {
      await reportesApi.eliminar(reporte.id);
      if (reportes.length === 1 && page > 1) setPage(page - 1);
      else listar();
    } catch {
      alert("Error al eliminar reporte");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "activo_nombre", label: "Activo", render: (row: Reporte) => <>{row.activo_nombre || "—"}</> },
    { key: "usuario_nombre", label: "Usuario", render: (row: Reporte) => <>{row.usuario_nombre || "—"}</> },
    { key: "tipo_incidencia", label: "Tipo" },
    {
      key: "descripcion",
      label: "Descripción",
      render: (row: Reporte) => <>{row.descripcion.length > 50 ? row.descripcion.slice(0, 50) + "..." : row.descripcion}</>,
    },
    { key: "fecha_reporte", label: "Fecha", render: (row: Reporte) => <>{formatDate(row.fecha_reporte)}</> },
    {
      key: "estado",
      label: "Estado",
      render: (row: Reporte) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Reportes de Incidencia</h2>
        <button onClick={() => navigate("/reportes/nuevo")} style={btnPrimary}>
          + Nuevo Reporte
        </button>
      </div>
      <DataTable
        columns={columns}
        data={reportes}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/reportes/editar/${row.id}`)}
        onDelete={eliminar}
      />
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
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
