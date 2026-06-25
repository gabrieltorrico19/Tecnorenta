import { type FormEvent, useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { usuarioApi, type UsuarioCreate, type UsuarioUpdate } from "../../api/usuario.api";
import FormField from "../../components/common/FormField";

export default function FormularioUsuario() {
  const navigate = useNavigate();
  const { id } = useParams();
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
      }).catch(() => alert("Error al cargar usuario"));
    }
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        const payload: UsuarioUpdate = { ...form };
        if (!payload.password) delete payload.password;
        await usuarioApi.actualizar(Number(id), payload);
      } else {
        await usuarioApi.crear(form);
      }
      navigate("/usuarios");
    } catch {
      alert("Error al guardar usuario");
    }
  };

  return (
    <div>
      <h2 style={styles.title}>{isEdit ? "Editar Usuario" : "Nuevo Usuario"}</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <FormField label="Nombre" required>
          <input
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            required
          />
        </FormField>
        <FormField label="Email" required>
          <input
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
        </FormField>
        <FormField label={isEdit ? "Contraseña (dejar vacío para no cambiar)" : "Contraseña"} required={!isEdit}>
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required={!isEdit}
          />
        </FormField>
        <FormField label="Teléfono">
          <input
            value={form.telefono}
            onChange={(e) => setForm({ ...form, telefono: e.target.value })}
          />
        </FormField>
        <div style={styles.actions}>
          <button type="submit" style={styles.btnGuardar}>Guardar</button>
          <button type="button" onClick={() => navigate("/usuarios")} style={styles.btnCancelar}>Cancelar</button>
        </div>
      </form>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  title: {
    fontSize: "1.4rem",
    fontWeight: 700,
    color: "var(--text-primary)",
    marginBottom: "1.5rem",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    maxWidth: "500px",
  },
  actions: {
    display: "flex",
    gap: "0.75rem",
    marginTop: "1rem",
  },
  btnGuardar: {
    background: "var(--accent)",
    color: "#fff",
    border: "none",
    padding: "0.6rem 1.2rem",
    borderRadius: "var(--radius-sm)",
    fontWeight: 600,
    cursor: "pointer",
  },
  btnCancelar: {
    background: "none",
    border: "1px solid var(--border)",
    color: "var(--text-secondary)",
    padding: "0.6rem 1.2rem",
    borderRadius: "var(--radius-sm)",
    cursor: "pointer",
  },
};
