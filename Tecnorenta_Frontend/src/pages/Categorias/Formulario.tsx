import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import { categoriasApi, type Categoria, type CategoriaCreate, type CategoriaUpdate } from "../../api/categorias.api";

export default function FormularioCategoria() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [nombre, setNombre] = useState("");
  const [nivel, setNivel] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [idCategoriaPadre, setIdCategoriaPadre] = useState("");
  const [categorias, setCategorias] = useState<Categoria[]>([]);

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
    try {
      if (isEdit) {
        const data: CategoriaUpdate = {
          nombre,
          nivel: nivel || undefined,
          descripcion: descripcion || undefined,
          id_categoria_padre: idCategoriaPadre ? Number(idCategoriaPadre) : null,
        };
        await categoriasApi.actualizar(Number(id), data);
      } else {
        const data: CategoriaCreate = {
          nombre,
          nivel: nivel || undefined,
          descripcion: descripcion || undefined,
          id_categoria_padre: idCategoriaPadre ? Number(idCategoriaPadre) : null,
        };
        await categoriasApi.crear(data);
      }
      navigate("/categorias");
    } catch {
      alert(`Error al ${isEdit ? "actualizar" : "crear"} la categoría`);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Categoría" : "Nueva Categoría"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Nombre" required>
          <input
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
            style={inputStyle}
          />
        </FormField>
        <FormField label="Nivel">
          <input
            value={nivel}
            onChange={(e) => setNivel(e.target.value)}
            placeholder="Ej: 1, 2, 3..."
            style={inputStyle}
          />
        </FormField>
        <FormField label="Descripción">
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            style={{ ...inputStyle, minHeight: 80, resize: "vertical" }}
          />
        </FormField>
        <FormField label="Categoría Padre">
          <select
            value={idCategoriaPadre}
            onChange={(e) => setIdCategoriaPadre(e.target.value)}
            style={inputStyle}
          >
            <option value="">-- Ninguna --</option>
            {categorias.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.nombre}
              </option>
            ))}
          </select>
        </FormField>
        <div style={actionsStyle}>
          <button type="submit" style={btnSave}>Guardar</button>
          <button type="button" onClick={() => navigate("/categorias")} style={btnCancel}>Cancelar</button>
        </div>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  maxWidth: "500px",
  marginTop: "1rem",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "0.9rem",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "0.5rem",
};

const btnSave: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.6rem 1.5rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
};

const btnCancel: React.CSSProperties = {
  background: "transparent",
  color: "var(--text-secondary)",
  border: "1px solid var(--border)",
  padding: "0.6rem 1.5rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
};
