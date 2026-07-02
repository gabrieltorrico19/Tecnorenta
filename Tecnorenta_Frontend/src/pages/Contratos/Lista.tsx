import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { contratosApi, type Contrato } from "../../api/contratos.api";
import { clientesApi } from "../../api/clientes.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import { formatCurrency } from "../../utils/helpers";
import { Plus } from "lucide-react";

const PAGE_SIZE = 20;

const estadoVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  activo: "success",
  vencido: "danger",
  cancelado: "danger",
  renovado: "default",
};

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-MX", { year: "numeric", month: "2-digit", day: "2-digit" });
}

export default function ListaContratos() {
  const navigate = useNavigate();
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [clientesMap, setClientesMap] = useState<Record<number, string>>({});
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [cRes, clientes] = await Promise.all([
        contratosApi.listar({ page, page_size: PAGE_SIZE }),
        clientesApi.listarTodos(),
      ]);
      setContratos(cRes.data.items);
      setPages(cRes.data.pages);
      setTotal(cRes.data.total);
      const cm: Record<number, string> = {};
      clientes.forEach((cl) => { cm[cl.id] = cl.nombre; });
      setClientesMap(cm);
    } catch {
      setError("Error al cargar contratos");
    } finally {
      setLoading(false);
    }
  }, [page]);

  const eliminar = useCallback(
    async (id: number) => {
      if (!window.confirm("¿Eliminar este contrato?")) return;
      try {
        await contratosApi.eliminar(id);
        if (contratos.length === 1 && page > 1) setPage(page - 1);
        else listar();
      } catch {
        alert("Error al eliminar contrato");
      }
    },
    [listar, contratos.length, page]
  );

  useEffect(() => {
    listar();
  }, [listar]);

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "cliente",
      label: "Cliente",
      render: (row: Contrato) => <>{clientesMap[row.id_cliente] || `ID ${row.id_cliente}`}</>,
    },
    {
      key: "fecha_inicio",
      label: "Inicio",
      render: (row: Contrato) => <>{formatDate(row.fecha_inicio)}</>,
    },
    {
      key: "fecha_fin",
      label: "Fin",
      render: (row: Contrato) => <>{formatDate(row.fecha_fin)}</>,
    },
    {
      key: "monto_mensual",
      label: "Monto Mensual",
      render: (row: Contrato) => <>{formatCurrency(row.monto_mensual)}</>,
    },
    {
      key: "estado",
      label: "Estado",
      render: (row: Contrato) => (
        <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Contratos</h2>
        <Button onClick={() => navigate("/contratos/nuevo")} icon={<Plus size={16} />}>Nuevo Contrato</Button>
      </div>
      <DataTable
        columns={columns}
        data={contratos}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/contratos/editar/${row.id}`)}
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
