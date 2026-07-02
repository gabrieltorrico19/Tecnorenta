import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { pagosApi, type Pago } from "../../api/pagos.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import { Plus } from "lucide-react";

const PAGE_SIZE = 20;

const estadoVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  pagado: "success",
  pendiente: "warning",
  atrasado: "danger",
  rechazado: "danger",
  anulado: "danger",
};

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-MX", { year: "numeric", month: "2-digit", day: "2-digit" });
}

export default function ListaPagos() {
  const navigate = useNavigate();
  const [pagos, setPagos] = useState<Pago[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await pagosApi.listar({ page, page_size: PAGE_SIZE });
      setPagos(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar pagos");
    } finally {
      setLoading(false);
    }
  }, [page]);

  const eliminar = useCallback(
    async (id: number) => {
      if (!window.confirm("¿Eliminar este pago?")) return;
      try {
        await pagosApi.eliminar(id);
        if (pagos.length === 1 && page > 1) setPage(page - 1);
        else listar();
      } catch {
        alert("Error al eliminar pago");
      }
    },
    [listar, pagos.length, page]
  );

  useEffect(() => {
    listar();
  }, [listar]);

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "id_contrato",
      label: "Contrato",
      render: (row: Pago) => <>{`#${row.id_contrato}`}</>,
    },
    { key: "concepto", label: "Concepto" },
    {
      key: "monto",
      label: "Monto",
      render: (row: Pago) => <>{`$ ${row.monto}`}</>,
    },
    {
      key: "fecha",
      label: "Fecha",
      render: (row: Pago) => <>{formatDate(row.fecha)}</>,
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Pago) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Pagos</h2>
        <Button onClick={() => navigate("/pagos/nuevo")} icon={<Plus size={16} />}>Nuevo Pago</Button>
      </div>
      <DataTable
        columns={columns}
        data={pagos}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/pagos/editar/${row.id}`)}
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
  marginBottom: "var(--space-md)",
};
