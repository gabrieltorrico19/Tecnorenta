import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { clientesApi, type Cliente } from "../../api/clientes.api";
import DataTable from "../../components/common/DataTable";
import Badge from "../../components/common/Badge";

export default function ListaClientes() {
  const navigate = useNavigate();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await clientesApi.listar();
      setClientes(res.data);
    } catch {
      setError("Error al cargar clientes");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = useCallback(
    async (cliente: Cliente) => {
      if (!window.confirm(`¿Eliminar cliente "${cliente.nombre}"?`)) return;
      try {
        await clientesApi.eliminar(cliente.id);
        listar();
      } catch {
        alert("Error al eliminar cliente");
      }
    },
    [listar]
  );

  const columns = [
    { key: "id", label: "ID" },
    {
      key: "documento",
      label: "Documento",
      render: (row: Cliente) => `${row.tipo_documento} ${row.numero_documento}`,
    },
    { key: "nombre", label: "Nombre" },
    { key: "email", label: "Email" },
    {
      key: "telefono",
      label: "Teléfono",
      render: (row: Cliente) => row.telefono ?? "—",
    },
    {
      key: "activo",
      label: "Activo",
      render: (row: Cliente) => (
        <Badge variant={row.activo ? "success" : "danger"}>
          {row.activo ? "Sí" : "No"}
        </Badge>
      ),
    },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2 style={titleStyle}>Clientes</h2>
        <button onClick={() => navigate("/clientes/nuevo")} style={btnNuevoStyle}>
          + Nuevo Cliente
        </button>
      </div>
      <DataTable
        columns={columns}
        data={clientes}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/clientes/editar/${row.id}`)}
        onDelete={eliminar}
      />
    </div>
  );
}

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "1.5rem",
};

const titleStyle: React.CSSProperties = {
  margin: 0,
};

const btnNuevoStyle: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.5rem 1rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.85rem",
};
