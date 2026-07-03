import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { mantenimientosApi, type Mantenimiento } from "../../api/mantenimientos.api";
import { activosApi } from "../../api/activos.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import FilterBar from "../../components/common/FilterBar";
import { formatDate, formatCurrency } from "../../utils/helpers";

const PAGE_SIZE = 20;

const tipoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  preventivo: "info",
  correctivo: "warning",
};

export default function ListaMantenimientos() {
  const navigate = useNavigate();
  const [mantenimientos, setMantenimientos] = useState<Mantenimiento[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activosMap, setActivosMap] = useState<Record<number, string>>({});
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);
  // filtros (server-side)
  const [tipo, setTipo] = useState("");

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await mantenimientosApi.listar({
        page,
        page_size: PAGE_SIZE,
        tipo: tipo || undefined,
      });
      setMantenimientos(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar mantenimientos");
    } finally {
      setLoading(false);
    }
  }, [page, tipo]);

  useEffect(() => {
    activosApi.listarTodos().then((items) => {
      const am: Record<number, string> = {};
      items.forEach((a) => { am[a.id] = `${a.codigo_inventario} - ${a.modelo}`; });
      setActivosMap(am);
    }).catch(() => { /* mapa opcional */ });
  }, []);

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
      key: "id_activo",
      label: "Activo",
      render: (row: Mantenimiento) => <>{activosMap[row.id_activo] || `ID ${row.id_activo}`}</>,
    },
    {
      key: "tipo",
      label: "Tipo",
      render: (row: Mantenimiento) => (
        <Badge variant={tipoVariant[row.tipo] || "default"}>{row.tipo}</Badge>
      ),
    },
    {
      key: "fecha",
      label: "Fecha",
      render: (row: Mantenimiento) => <>{formatDate(row.fecha)}</>,
    },
    {
      key: "costo",
      label: "Costo",
      render: (row: Mantenimiento) => <>{formatCurrency(row.costo ?? 0, 2)}</>,
    },
    {
      key: "proxima_fecha",
      label: "Próxima",
      render: (row: Mantenimiento) => <>{row.proxima_fecha ? formatDate(row.proxima_fecha) : "—"}</>,
    },
    {
      key: "descripcion",
      label: "Descripción",
      render: (row: Mantenimiento) => {
        const d = row.descripcion ?? "—";
        return <>{d.length > 50 ? `${d.slice(0, 50)}…` : d}</>;
      },
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
      <FilterBar hayFiltros={tipo !== ""} onLimpiar={() => { setTipo(""); setPage(1); }}>
        <select value={tipo} onChange={(e) => { setTipo(e.target.value); setPage(1); }}>
          <option value="">Todos los tipos</option>
          <option value="preventivo">Preventivo</option>
          <option value="correctivo">Correctivo</option>
        </select>
      </FilterBar>
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
