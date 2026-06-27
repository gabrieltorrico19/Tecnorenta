import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { contratosApi, type Contrato } from "../../api/contratos.api";
import { clientesApi } from "../../api/clientes.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import { Plus } from "lucide-react";

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

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [cRes, clRes] = await Promise.all([
        contratosApi.listar(),
        clientesApi.listar(),
      ]);
      setContratos(cRes.data);
      const cm: Record<number, string> = {};
      clRes.data.forEach((cl: { id: number; nombre: string }) => { cm[cl.id] = cl.nombre; });
      setClientesMap(cm);
    } catch {
      setError("Error al cargar contratos");
    } finally {
      setLoading(false);
    }
  }, []);

  const eliminar = useCallback(
    async (id: number) => {
      if (!window.confirm("¿Eliminar este contrato?")) return;
      try {
        await contratosApi.eliminar(id);
        setContratos((prev) => prev.filter((c) => c.id !== id));
      } catch {
        alert("Error al eliminar contrato");
      }
    },
    []
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
      render: (row: Contrato) => <>{`$ ${row.monto_mensual}`}</>,
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
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
