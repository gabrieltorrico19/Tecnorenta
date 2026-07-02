import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { clientesApi, type Cliente } from "../../api/clientes.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";

const PAGE_SIZE = 20;

export default function ListaClientes() {
  const navigate = useNavigate();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await clientesApi.listar({ page, page_size: PAGE_SIZE });
      setClientes(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar clientes");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    listar();
  }, [listar]);

  const eliminar = useCallback(
    async (cliente: Cliente) => {
      if (!window.confirm(`¿Eliminar cliente "${cliente.nombre}"?`)) return;
      try {
        await clientesApi.eliminar(cliente.id);
        if (clientes.length === 1 && page > 1) setPage(page - 1);
        else listar();
      } catch {
        alert("Error al eliminar cliente");
      }
    },
    [listar, clientes.length, page]
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
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
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
