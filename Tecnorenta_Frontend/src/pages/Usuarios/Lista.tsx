import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { usuarioApi, type Usuario } from "../../api/usuario.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import { formatDate } from "../../utils/helpers";

const PAGE_SIZE = 20;

export default function ListaUsuarios() {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await usuarioApi.listar({ page, page_size: PAGE_SIZE });
      setUsuarios(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => { listar(); }, [listar]);

  const eliminar = async (id: number) => {
    if (!window.confirm("¿Eliminar este usuario?")) return;
    try {
      await usuarioApi.eliminar(id);
      if (usuarios.length === 1 && page > 1) setPage(page - 1);
      else listar();
    } catch {
      alert("Error al eliminar usuario");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "nombre", label: "Nombre" },
    { key: "email", label: "Email" },
    { key: "telefono", label: "Teléfono", render: (row: Usuario) => row.telefono || "—" },
    {
      key: "activo", label: "Estado",
      render: (row: Usuario) => row.activo
        ? <Badge variant="success">Activo</Badge>
        : <Badge variant="danger">Inactivo</Badge>,
    },
    {
      key: "created_at", label: "Creado",
      render: (row: Usuario) => formatDate(row.created_at),
    },
  ];

  return (
    <div>
      <div style={styles.topBar}>
        <h2 style={styles.title}>Usuarios</h2>
        <button onClick={() => navigate("/usuarios/nuevo")} style={styles.btnNuevo}>
          + Nuevo Usuario
        </button>
      </div>
      <DataTable
        columns={columns}
        data={usuarios}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/usuarios/editar/${row.id}`)}
        onDelete={(row) => eliminar(row.id)}
      />
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "1.5rem",
  },
  title: {
    fontSize: "1.4rem",
    fontWeight: 700,
    color: "var(--text-primary)",
  },
  btnNuevo: {
    background: "var(--accent)",
    color: "#fff",
    border: "none",
    padding: "0.5rem 1rem",
    borderRadius: "var(--radius-sm)",
    fontWeight: 600,
    cursor: "pointer",
  },
};
