import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { reportesApi, type Reporte } from "../../api/reportes.api";
import { activosApi } from "../../api/activos.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import FilterBar from "../../components/common/FilterBar";
import { formatDate } from "../../utils/helpers";

const PAGE_SIZE = 20;

const gravedadVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  leve: "info",
  moderado: "warning",
  grave: "danger",
};

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  abierto: "danger",
  en_atencion: "warning",
  cerrado: "success",
};

export default function ListaReportes() {
  const navigate = useNavigate();
  const [reportes, setReportes] = useState<Reporte[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activosMap, setActivosMap] = useState<Record<number, string>>({});
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);
  // filtros (server-side)
  const [gravedad, setGravedad] = useState("");
  const [estado, setEstado] = useState("");

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await reportesApi.listar({
        page,
        page_size: PAGE_SIZE,
        gravedad: gravedad || undefined,
        estado: estado || undefined,
      });
      setReportes(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar reportes");
    } finally {
      setLoading(false);
    }
  }, [page, gravedad, estado]);

  useEffect(() => {
    listar();
  }, [listar]);

  useEffect(() => {
    activosApi.listarTodos().then((items) => {
      const am: Record<number, string> = {};
      items.forEach((a) => { am[a.id] = `${a.codigo_inventario} - ${a.modelo}`; });
      setActivosMap(am);
    }).catch(() => { /* mapa opcional */ });
  }, []);

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

  const hayFiltros = gravedad !== "" || estado !== "";

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "id_activo",
      label: "Activo",
      render: (row: Reporte) => <>{activosMap[row.id_activo] || `ID ${row.id_activo}`}</>,
    },
    { key: "fecha", label: "Fecha", render: (row: Reporte) => <>{formatDate(row.fecha)}</> },
    {
      key: "gravedad",
      label: "Gravedad",
      render: (row: Reporte) => (
        <Badge variant={gravedadVariant[row.gravedad] || "default"}>{row.gravedad}</Badge>
      ),
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Reporte) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado.replace("_", " ")}</Badge>
      ),
    },
    {
      key: "descripcion",
      label: "Descripción",
      render: (row: Reporte) => <>{row.descripcion.length > 50 ? row.descripcion.slice(0, 50) + "..." : row.descripcion}</>,
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
      <FilterBar
        hayFiltros={hayFiltros}
        onLimpiar={() => { setGravedad(""); setEstado(""); setPage(1); }}
      >
        <select value={gravedad} onChange={(e) => { setGravedad(e.target.value); setPage(1); }}>
          <option value="">Todas las gravedades</option>
          <option value="leve">Leve</option>
          <option value="moderado">Moderado</option>
          <option value="grave">Grave</option>
        </select>
        <select value={estado} onChange={(e) => { setEstado(e.target.value); setPage(1); }}>
          <option value="">Todos los estados</option>
          <option value="abierto">Abierto</option>
          <option value="en_atencion">En atención</option>
          <option value="cerrado">Cerrado</option>
        </select>
      </FilterBar>
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
