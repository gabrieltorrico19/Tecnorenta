import { useState, useEffect, type FormEvent } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  clientesApi,
  type ClienteCreate,
  type ClienteUpdate,
} from "../../api/clientes.api";
import FormField from "../../components/common/FormField";

type Modo = "crear" | "editar";

export default function FormularioCliente() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const modo: Modo = id ? "editar" : "crear";

  const [form, setForm] = useState<ClienteCreate>({
    tipo_persona: "Natural",
    tipo_documento: "DNI",
    numero_documento: "",
    nombre: "",
    email: "",
    telefono: "",
    direccion: "",
  });

  useEffect(() => {
    if (!id) return;
    clientesApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setForm({
        tipo_persona: c.tipo_persona,
        tipo_documento: c.tipo_documento,
        numero_documento: c.numero_documento,
        nombre: c.nombre,
        email: c.email,
        telefono: c.telefono ?? "",
        direccion: c.direccion ?? "",
      });
    });
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (modo === "crear") {
        await clientesApi.crear(form);
      } else {
        const payload: ClienteUpdate = {
          nombre: form.nombre,
          email: form.email,
          telefono: form.telefono,
          direccion: form.direccion,
        };
        await clientesApi.actualizar(Number(id), payload);
      }
      navigate("/clientes");
    } catch {
      alert("Error al guardar cliente");
    }
  };

  const set = (field: keyof ClienteCreate) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setForm({ ...form, [field]: e.target.value });

  return (
    <div>
      <h2 style={titleStyle}>
        {modo === "crear" ? "Nuevo Cliente" : "Editar Cliente"}
      </h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Tipo de Persona" required>
          <select value={form.tipo_persona} onChange={set("tipo_persona")} style={inputStyle}>
            <option value="Natural">Natural</option>
            <option value="Jurídica">Jurídica</option>
          </select>
        </FormField>

        <FormField label="Tipo de Documento" required>
          <select value={form.tipo_documento} onChange={set("tipo_documento")} style={inputStyle}>
            <option value="DNI">DNI</option>
            <option value="RUC">RUC</option>
            <option value="Carné Extranjería">Carné Extranjería</option>
          </select>
        </FormField>

        <FormField label="Número de Documento" required>
          <input
            type="text"
            value={form.numero_documento}
            onChange={set("numero_documento")}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Nombre" required>
          <input
            type="text"
            value={form.nombre}
            onChange={set("nombre")}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Email" required>
          <input
            type="email"
            value={form.email}
            onChange={set("email")}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Teléfono">
          <input
            type="text"
            value={form.telefono}
            onChange={set("telefono")}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Dirección">
          <textarea
            value={form.direccion}
            onChange={set("direccion")}
            style={{ ...inputStyle, minHeight: 80, resize: "vertical" }}
          />
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnSaveStyle}>
            Guardar
          </button>
          <button type="button" onClick={() => navigate("/clientes")} style={btnCancelStyle}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

const titleStyle: React.CSSProperties = {
  marginBottom: "1.5rem",
};

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  maxWidth: "500px",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--surface)",
  color: "var(--text)",
  fontSize: "0.9rem",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "0.5rem",
};

const btnSaveStyle: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.6rem 1.5rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.9rem",
};

const btnCancelStyle: React.CSSProperties = {
  background: "transparent",
  color: "var(--text-secondary)",
  border: "1px solid var(--border)",
  padding: "0.6rem 1.5rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.9rem",
};
