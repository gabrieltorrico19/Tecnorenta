import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { activosApi, type Activo } from "../../api/activos.api";
import { categoriasApi, type Categoria } from "../../api/categorias.api";
import DataTable from "../../components/common/DataTable";
import Pagination from "../../components/common/Pagination";
import Badge from "../../components/common/Badge";
import Button from "../../components/common/Button";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import FilterBar from "../../components/common/FilterBar";
import { useToast } from "../../context/ToastContext";
import { Plus, Download } from "lucide-react";

const PAGE_SIZE = 20;

const estadoVariant: Record<string, "success" | "warning" | "danger" | "info" | "default"> = {
  disponible: "success",
  rentado: "warning",
  mantenimiento: "warning",
  baja: "danger",
};

export default function ListaActivos() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [activos, setActivos] = useState<Activo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Activo | null>(null);
  const [fotosMap, setFotosMap] = useState<Record<number, string>>({});
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [total, setTotal] = useState(0);
  // filtros (server-side)
  const [estado, setEstado] = useState("");
  const [idCategoria, setIdCategoria] = useState("");
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [q, setQ] = useState("");
  const [qAplicado, setQAplicado] = useState("");

  // debounce de la búsqueda: aplica 400 ms después de dejar de escribir
  useEffect(() => {
    const t = setTimeout(() => {
      setQAplicado(q);
      setPage(1);
    }, 400);
    return () => clearTimeout(t);
  }, [q]);

  useEffect(() => {
    categoriasApi.listarTodos().then(setCategorias).catch(() => { /* catálogo opcional */ });
  }, []);

  const cargarPrimeraFoto = useCallback(async (activo: Activo) => {
    try {
      const res = await activosApi.listarFotos(activo.id);
      if (res.data.length > 0) {
        setFotosMap((prev) => ({ ...prev, [activo.id]: res.data[0].url }));
      }
    } catch { /* ignore */ }
  }, []);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await activosApi.listar({
        page,
        page_size: PAGE_SIZE,
        estado: estado || undefined,
        id_categoria: idCategoria ? Number(idCategoria) : undefined,
        q: qAplicado || undefined,
      });
      setActivos(res.data.items);
      setPages(res.data.pages);
      setTotal(res.data.total);
    } catch {
      setError("Error al cargar activos");
    } finally {
      setLoading(false);
    }
  }, [page, estado, idCategoria, qAplicado]);

  useEffect(() => { listar(); }, [listar]);

  useEffect(() => {
    activos.forEach((a) => { if (!fotosMap[a.id]) cargarPrimeraFoto(a); });
  }, [activos, fotosMap, cargarPrimeraFoto]);

  const eliminar = async (activo: Activo) => {
    try {
      await activosApi.eliminar(activo.id);
      toast("Activo eliminado correctamente", "success");
      if (activos.length === 1 && page > 1) setPage(page - 1);
      else listar();
    } catch {
      toast("Error al eliminar el activo", "error");
    }
    setDeleteTarget(null);
  };

  const columns = [
    {
      key: "foto",
      label: "Foto",
      render: (row: Activo) => {
        const url = fotosMap[row.id];
        return url ? (
          <img src={`http://localhost:8000/static/${url}`} alt="" style={thumbCol} />
        ) : (
          <span style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>—</span>
        );
      },
    },
    { key: "id", label: "ID" },
    { key: "codigo_inventario", label: "Código" },
    { key: "modelo", label: "Modelo" },
    { key: "categoria_nombre", label: "Categoría", render: (row: Activo) => <>{row.categoria_nombre || "—"}</> },
    { key: "estado", label: "Estado", render: (row: Activo) => <Badge variant={estadoVariant[row.estado] || "default"}>{row.estado}</Badge> },
    { key: "numero_serie", label: "Serie", render: (row: Activo) => <>{row.numero_serie || "—"}</> },
  ];

  return (
    <div>
      <div style={headerStyle}>
        <h2>Activos</h2>
        <div style={{ display: "flex", gap: "var(--space-sm)" }}>
          <a href={activosApi.exportarCsv()} style={{ textDecoration: "none" }}>
            <Button variant="secondary" icon={<Download size={16} />}>Exportar CSV</Button>
          </a>
          <Button onClick={() => navigate("/activos/nuevo")} icon={<Plus size={16} />}>Nuevo Activo</Button>
        </div>
      </div>
      <FilterBar
        hayFiltros={estado !== "" || idCategoria !== "" || q !== ""}
        onLimpiar={() => { setEstado(""); setIdCategoria(""); setQ(""); setPage(1); }}
      >
        <input
          type="search"
          placeholder="Buscar código, modelo o serie…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ minWidth: 240 }}
        />
        <select value={estado} onChange={(e) => { setEstado(e.target.value); setPage(1); }}>
          <option value="">Todos los estados</option>
          <option value="disponible">Disponible</option>
          <option value="rentado">Rentado</option>
          <option value="mantenimiento">Mantenimiento</option>
          <option value="baja">Baja</option>
        </select>
        <select value={idCategoria} onChange={(e) => { setIdCategoria(e.target.value); setPage(1); }}>
          <option value="">Todas las categorías</option>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>{c.nombre}</option>
          ))}
        </select>
      </FilterBar>
      <DataTable columns={columns} data={activos} loading={loading} error={error}
        onEdit={(row) => navigate(`/activos/editar/${row.id}`)}
        onDelete={(row) => setDeleteTarget(row)}
      />
      <Pagination page={page} pages={pages} total={total} pageSize={PAGE_SIZE} onPageChange={setPage} />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Eliminar activo"
        message={`¿Está seguro de eliminar el activo "${deleteTarget?.modelo}"?`}
        onConfirm={() => deleteTarget && eliminar(deleteTarget)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}

const thumbCol: React.CSSProperties = {
  width: 40,
  height: 40,
  borderRadius: "var(--radius-sm)",
  objectFit: "cover",
  border: "1px solid var(--border)",
};

const headerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
