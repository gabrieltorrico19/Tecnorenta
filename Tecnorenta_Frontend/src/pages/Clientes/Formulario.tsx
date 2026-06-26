import { useState, useEffect, type FormEvent } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { clientesApi, type ClienteCreate, type ClienteUpdate } from "../../api/clientes.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

type Modo = "crear" | "editar";

export default function FormularioCliente() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
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
    }).catch(() => toast("Error al cargar cliente", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (modo === "crear") {
        await clientesApi.crear(form);
        toast("Cliente creado", "success");
      } else {
        const payload: ClienteUpdate = {
          nombre: form.nombre,
          email: form.email,
          telefono: form.telefono,
          direccion: form.direccion,
        };
        await clientesApi.actualizar(Number(id), payload);
        toast("Cliente actualizado", "success");
      }
      navigate("/clientes");
    } catch {
      toast("Error al guardar cliente", "error");
    }
  };

  const set = (field: keyof ClienteCreate) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setForm({ ...form, [field]: e.target.value });

  return (
    <div>
      <h2>{modo === "crear" ? "Nuevo Cliente" : "Editar Cliente"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Identificación">
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
            <input type="text" value={form.numero_documento} onChange={set("numero_documento")} required style={inputStyle} />
          </FormField>
        </FormSection>
        <FormSection title="Información de Contacto">
          <FormField label="Nombre" required>
            <input type="text" value={form.nombre} onChange={set("nombre")} required style={inputStyle} />
          </FormField>
          <FormField label="Email" required>
            <input type="email" value={form.email} onChange={set("email")} required style={inputStyle} />
          </FormField>
          <FormField label="Teléfono">
            <input type="text" value={form.telefono} onChange={set("telefono")} style={inputStyle} />
          </FormField>
          <FormField label="Dirección">
            <textarea value={form.direccion} onChange={set("direccion")} style={{ ...inputStyle, minHeight: 80, resize: "vertical" }} />
          </FormField>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/clientes")}>Cancelar</Button>
        </div>
      </form>
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "var(--font-size-md)",
  width: "100%",
  boxSizing: "border-box",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "var(--space-lg)",
};
