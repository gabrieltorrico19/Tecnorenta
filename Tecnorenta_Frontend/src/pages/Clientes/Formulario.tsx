import { useState, useEffect, type FormEvent } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { clientesApi, type ClienteCreate } from "../../api/clientes.api";
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
    razon_social: "",
    nit: "",
    direccion: "",
    sector: "",
  });

  useEffect(() => {
    if (!id) return;
    clientesApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setForm({
        razon_social: c.razon_social,
        nit: c.nit,
        direccion: c.direccion ?? "",
        sector: c.sector ?? "",
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
        await clientesApi.actualizar(Number(id), form);
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
          <FormField label="Razón Social" required>
            <input type="text" value={form.razon_social} onChange={set("razon_social")} required style={inputStyle} />
          </FormField>
          <FormField label="NIT" required>
            <input type="text" value={form.nit} onChange={set("nit")} required style={inputStyle} />
          </FormField>
        </FormSection>
        <FormSection title="Ubicación">
          <FormField label="Sector">
            <input type="text" value={form.sector} onChange={set("sector")} style={inputStyle} placeholder="Ej. Equipetrol, Centro…" />
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
