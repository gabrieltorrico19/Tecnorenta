import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { mantenimientosApi, type Mantenimiento } from "../../api/mantenimientos.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import { formatDate } from "../../utils/helpers";

const PAGE_SIZE = 20;

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  Pendiente: "warning",
  "En Progreso": "info",
  Completado: "success",
  Cancelado: "danger",
};

export default function ListaMantenimientos() {
  const navigate = useNavigate();
  const [mantenimientos, setMantenimientos] = useState<Mantenimiento[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await mantenimientosApi.listar({ page, page_size: PAGE_SIZE });
      setMantenimientos(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar mantenimientos");
    } finally {
      setLoading(false);
    }
  }, [page]);

  const eliminar = useCallback(
    async (id: number) => {
      if (!window.confirm("¿Eliminar este mantenimiento?")) return;
      try {
        await mantenimientosApi.eliminar(id);
        if (mantenimientos.length === 1 && page > 1) setPage(page - 1);
        else listar();
      } catch {
        alert("Error al eliminar mantenimiento");
      }
    },
    [listar, mantenimientos.length, page]
  );

  useEffect(() => {
    listar();
  }, [listar]);

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "activo_nombre",
      label: "Activo",
      render: (row: Mantenimiento) => <>{row.activo_nombre || "—"}</>,
    },
    { key: "tipo_mantenimiento", label: "Tipo" },
    {
      key: "descripcion",
      label: "Descripción",
      render: (row: Mantenimiento) => (
        <>{row.descripcion.length > 50 ? `${row.descripcion.slice(0, 50)}…` : row.descripcion}</>
      ),
    },
    {
      key: "fecha_inicio",
      label: "Inicio",
      render: (row: Mantenimiento) => <>{row.fecha_inicio ? formatDate(row.fecha_inicio) : "—"}</>,
    },
    {
      key: "fecha_fin",
      label: "Fin",
      render: (row: Mantenimiento) => <>{row.fecha_fin ? formatDate(row.fecha_fin) : "—"}</>,
    },
    {
      key: "costo",
      label: "Costo",
      render: (row: Mantenimiento) => <>{row.costo != null ? `$ ${row.costo}` : "—"}</>,
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Mantenimiento) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Mantenimientos</h2>
        <button onClick={() => navigate("/mantenimientos/nuevo")} style={btnPrimary}>
          Nuevo Mantenimiento
        </button>
      </div>
      <DataTable
        columns={columns}
        data={mantenimientos}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/mantenimientos/editar/${row.id}`)}
        onDelete={(row) => eliminar(row.id)}
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
};
