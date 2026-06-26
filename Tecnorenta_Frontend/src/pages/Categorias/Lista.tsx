import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import DataTable from "../../components/common/DataTable";
import { categoriasApi, type Categoria } from "../../api/categorias.api";

function useCategorias() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await categoriasApi.listar();
      setCategorias(res.data);
    } catch {
      setError("Error al cargar categorías");
    } finally {
      setLoading(false);
    }
  }, []);

  const eliminar = useCallback(async (id: number) => {
    if (!window.confirm("¿Está seguro de eliminar esta categoría?")) return;
    try {
      await categoriasApi.eliminar(id);
      setCategorias((prev) => prev.filter((c) => c.id !== id));
    } catch {
      alert("Error al eliminar la categoría");
    }
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  return { categorias, loading, error, eliminar };
}

const columns = [
  { key: "id", label: "ID" },
  { key: "nombre", label: "Nombre" },
  { key: "nivel", label: "Nivel" },
  { key: "descripcion", label: "Descripción" },
];

export default function ListaCategorias() {
  const navigate = useNavigate();
  const { categorias, loading, error, eliminar } = useCategorias();

  return (
    <div>
      <div style={topBar}>
        <h2 style={{ margin: 0 }}>Categorías</h2>
        <button onClick={() => navigate("/categorias/nuevo")} style={btnNuevo}>
          + Nueva Categoría
        </button>
      </div>
      <DataTable
        columns={columns}
        data={categorias}
        loading={loading}
        error={error}
        onEdit={(row) => navigate(`/categorias/editar/${row.id}`)}
        onDelete={(row) => eliminar(row.id)}
      />
    </div>
  );
}

const topBar: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "1rem",
};

const btnNuevo: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.5rem 1rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.85rem",
};
