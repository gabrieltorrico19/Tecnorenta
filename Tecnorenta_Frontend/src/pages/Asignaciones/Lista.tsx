import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { asignacionesApi, type Asignacion } from "../../api/asignaciones.api";
import { contratosApi } from "../../api/contratos.api";
import { activosApi } from "../../api/activos.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Button from "../../components/common/Button";
import { Plus } from "lucide-react";

const PAGE_SIZE = 20;

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-MX", { year: "numeric", month: "2-digit", day: "2-digit" });
}

export default function ListaAsignaciones() {
  const navigate = useNavigate();
  const [asignaciones, setAsignaciones] = useState<Asignacion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [contratosMap, setContratosMap] = useState<Record<number, string>>({});
  const [activosMap, setActivosMap] = useState<Record<number, string>>({});
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [res, contratos, activos] = await Promise.all([
        asignacionesApi.listar({ page, page_size: PAGE_SIZE }),
        contratosApi.listarTodos(),
        activosApi.listarTodos(),
      ]);
      setAsignaciones(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
      const cm: Record<number, string> = {};
      contratos.forEach((c) => { cm[c.id] = `Contrato #${c.id}`; });
      setContratosMap(cm);
      const am: Record<number, string> = {};
      activos.forEach((a) => { am[a.id] = `${a.codigo_inventario} - ${a.modelo}`; });
      setActivosMap(am);
    } catch {
      setError("Error al cargar asignaciones");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = async (asignacion: Asignacion) => {
    if (!window.confirm(`¿Eliminar asignación #${asignacion.id}?`)) return;
    try {
      await asignacionesApi.eliminar(asignacion.id);
      if (asignaciones.length === 1 && page > 1) setPage(page - 1);
      else listar();
    } catch {
      alert("Error al eliminar asignación");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "id_activo", label: "ID Activo" },
    {
      key: "activo_nombre",
      label: "Activo",
      render: (row: Asignacion) => <>{activosMap[row.id_activo] || `ID ${row.id_activo}`}</>,
    },
    { key: "id_contrato", label: "ID Contrato" },
    {
      key: "contrato_nombre",
      label: "Contrato",
      render: (row: Asignacion) => <>{contratosMap[row.id_contrato] || `ID ${row.id_contrato}`}</>,
    },
    {
      key: "fecha_asignacion",
      label: "Fecha Asignación",
      render: (row: Asignacion) => <>{formatDate(row.fecha_asignacion)}</>,
    },
    {
      key: "fecha_devolucion",
      label: "Fecha Devolución",
      render: (row: Asignacion) => <>{formatDate(row.fecha_devolucion)}</>,
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Asignaciones</h2>
        <Button onClick={() => navigate("/asignaciones/nuevo")} icon={<Plus size={16} />}>Nueva Asignación</Button>
      </div>
      <DataTable
        columns={columns}
        data={asignaciones}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/asignaciones/editar/${row.id}`)}
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
  marginBottom: "var(--space-md)",
};
