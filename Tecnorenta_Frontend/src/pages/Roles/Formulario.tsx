import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import Button from "../../components/common/Button";
import { rolesApi, type RolCreate, type RolUpdate } from "../../api/roles.api";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioRol() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    rolesApi.obtener(Number(id)).then((res) => {
      setNombre(res.data.nombre);
      setDescripcion(res.data.descripcion ?? "");
    }).catch(() => alert("Error al cargar el rol"));
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const data: RolUpdate = { nombre, descripcion: descripcion || undefined };
        await rolesApi.actualizar(Number(id), data);
      } else {
        const data: RolCreate = { nombre, descripcion: descripcion || undefined };
        await rolesApi.crear(data);
      }
      navigate("/roles");
    } catch {
      alert(`Error al ${isEdit ? "actualizar" : "crear"} el rol`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Rol" : "Nuevo Rol"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Nombre" required>
          <input
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
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
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/roles")}>
            Cancelar
          </Button>
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
