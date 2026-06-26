import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import Button from "../../components/common/Button";
import { categoriasApi, type Categoria, type CategoriaCreate, type CategoriaUpdate } from "../../api/categorias.api";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioCategoria() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [nombre, setNombre] = useState("");
  const [nivel, setNivel] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [idCategoriaPadre, setIdCategoriaPadre] = useState("");
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    categoriasApi.listar().then((res) => {
      setCategorias(res.data.filter((c) => c.id !== Number(id)));
    }).catch(() => {});
  }, [id]);

  useEffect(() => {
    if (!id) return;
    categoriasApi.obtener(Number(id)).then((res) => {
      setNombre(res.data.nombre);
      setNivel(res.data.nivel ?? "");
      setDescripcion(res.data.descripcion ?? "");
      setIdCategoriaPadre(res.data.id_categoria_padre ? String(res.data.id_categoria_padre) : "");
    }).catch(() => alert("Error al cargar la categoría"));
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const data: CategoriaUpdate = { nombre, nivel: nivel || undefined, descripcion: descripcion || undefined, id_categoria_padre: idCategoriaPadre ? Number(idCategoriaPadre) : null };
        await categoriasApi.actualizar(Number(id), data);
      } else {
        const data: CategoriaCreate = { nombre, nivel: nivel || undefined, descripcion: descripcion || undefined, id_categoria_padre: idCategoriaPadre ? Number(idCategoriaPadre) : null };
        await categoriasApi.crear(data);
      }
      navigate("/categorias");
    } catch {
      alert(`Error al ${isEdit ? "actualizar" : "crear"} la categoría`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Categoría" : "Nueva Categoría"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Nombre" required>
          <input value={nombre} onChange={(e) => setNombre(e.target.value)} required style={inputStyle} />
        </FormField>
        <FormField label="Nivel">
          <input value={nivel} onChange={(e) => setNivel(e.target.value)} placeholder="Ej: 1, 2, 3..." style={inputStyle} />
        </FormField>
        <FormField label="Descripción">
          <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} style={{ ...inputStyle, minHeight: 80, resize: "vertical" }} />
        </FormField>
        <FormField label="Categoría Padre">
          <select value={idCategoriaPadre} onChange={(e) => setIdCategoriaPadre(e.target.value)} style={inputStyle}>
            <option value="">-- Ninguna --</option>
            {categorias.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.nombre}</option>
            ))}
          </select>
        </FormField>
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/categorias")}>Cancelar</Button>
        </div>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "var(--space-md)",
  maxWidth: "500px",
  marginTop: "var(--space-md)",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "var(--font-size-md)",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "0.5rem",
};
