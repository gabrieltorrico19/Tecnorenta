import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { pagosApi, type Pago } from "../../api/pagos.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";
import { formatDate } from "../../utils/helpers";

const estadoVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  Pagado: "success",
  Completado: "success",
  Pendiente: "warning",
  Atrasado: "danger",
  Rechazado: "danger",
};

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
      key: "contrato_numero",
      label: "Contrato",
      render: (row: Pago) => <>{row.contrato_numero || "—"}</>,
    },
    {
      key: "monto",
      label: "Monto",
      render: (row: Pago) => <>{`$ ${row.monto}`}</>,
    },
    {
      key: "fecha_pago",
      label: "Fecha Pago",
      render: (row: Pago) => <>{formatDate(row.fecha_pago)}</>,
    },
    { key: "metodo_pago", label: "Método Pago" },
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
        <button onClick={() => navigate("/pagos/nuevo")} style={btnPrimary}>
          Nuevo Pago
        </button>
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
