import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { contratosApi, type Contrato } from "../../api/contratos.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import { formatDate } from "../../utils/helpers";

const estadoVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  Activo: "success",
  Pendiente: "warning",
  Vencido: "danger",
  Cancelado: "danger",
};

export default function ListaContratos() {
  const navigate = useNavigate();
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await contratosApi.listar();
      setContratos(res.data);
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
    { key: "numero_contrato", label: "Número" },
    {
      key: "cliente_nombre",
      label: "Cliente",
      render: (row: Contrato) => <>{row.cliente_nombre || "—"}</>,
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
      key: "monto_total",
      label: "Monto Total",
      render: (row: Contrato) => <>{`$ ${row.monto_total}`}</>,
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
        <button onClick={() => navigate("/contratos/nuevo")} style={btnPrimary}>
          Nuevo Contrato
        </button>
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
