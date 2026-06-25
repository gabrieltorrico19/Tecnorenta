import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import { rolesApi, type RolCreate, type RolUpdate } from "../../api/roles.api";

export default function FormularioRol() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");

  useEffect(() => {
    if (!id) return;
    rolesApi.obtener(Number(id)).then((res) => {
      setNombre(res.data.nombre);
      setDescripcion(res.data.descripcion ?? "");
    }).catch(() => alert("Error al cargar el rol"));
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
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
          <button type="submit" style={btnSave}>Guardar</button>
          <button type="button" onClick={() => navigate("/roles")} style={btnCancel}>Cancelar</button>
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
