import { type FormEvent, useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { usuarioApi, type UsuarioCreate, type UsuarioUpdate } from "../../api/usuario.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioUsuario() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { toast } = useToast();
  const isEdit = !!id;

  const [form, setForm] = useState<UsuarioCreate>({
    nombre: "",
    email: "",
    password: "",
    telefono: "",
  });

  useEffect(() => {
    if (id) {
      usuarioApi.obtener(Number(id)).then((res) => {
        setForm({
          nombre: res.data.nombre,
          email: res.data.email,
          password: "",
          telefono: res.data.telefono || "",
        });
      }).catch(() => toast("Error al cargar usuario", "error"));
    }
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        const payload: UsuarioUpdate = { ...form };
        if (!payload.password) delete payload.password;
        await usuarioApi.actualizar(Number(id), payload);
        toast("Usuario actualizado", "success");
      } else {
        await usuarioApi.crear(form);
        toast("Usuario creado", "success");
      }
      navigate("/usuarios");
    } catch {
      toast("Error al guardar usuario", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Usuario" : "Nuevo Usuario"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información del Usuario">
          <FormField label="Nombre" required>
            <input style={inputStyle} value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
          </FormField>
          <FormField label="Email" required>
            <input type="email" style={inputStyle} value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </FormField>
          <FormField label={isEdit ? "Contraseña (dejar vacío para no cambiar)" : "Contraseña"} required={!isEdit}>
            <input type="password" style={inputStyle} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required={!isEdit} />
          </FormField>
          <FormField label="Teléfono">
            <input style={inputStyle} value={form.telefono} onChange={(e) => setForm({ ...form, telefono: e.target.value })} />
          </FormField>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/usuarios")}>Cancelar</Button>
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
