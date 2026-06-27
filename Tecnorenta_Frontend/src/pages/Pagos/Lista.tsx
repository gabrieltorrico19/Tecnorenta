import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { pagosApi, type Pago } from "../../api/pagos.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import { Plus } from "lucide-react";

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

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await pagosApi.listar();
      setPagos(res.data);
    } catch {
      setError("Error al cargar pagos");
    } finally {
      setLoading(false);
    }
  }, []);

  const eliminar = useCallback(async (id: number) => {
    if (!window.confirm("¿Eliminar este pago?")) return;
    try {
      await pagosApi.eliminar(id);
      setPagos((prev) => prev.filter((p) => p.id !== id));
    } catch {
      alert("Error al eliminar pago");
    }
  }, []);

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
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
