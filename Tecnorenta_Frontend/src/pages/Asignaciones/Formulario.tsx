import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { asignacionesApi, type AsignacionCreate, type AsignacionUpdate } from "../../api/asignaciones.api";
import FormField from "../../components/common/FormField";

const ESTADOS = ["Activa", "Pendiente", "Devuelta", "Cancelada"];

export default function FormularioAsignacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<AsignacionCreate>({
    activo_id: 0,
    usuario_id: 0,
    fecha_asignacion: "",
    fecha_devolucion: "",
    motivo: "",
    estado: "Activa",
  });

  useEffect(() => {
    if (!id) return;
    asignacionesApi.obtener(Number(id)).then((res) => {
      const a = res.data;
      setForm({
        activo_id: a.activo_id,
        usuario_id: a.usuario_id,
        fecha_asignacion: a.fecha_asignacion,
        fecha_devolucion: a.fecha_devolucion || "",
        motivo: a.motivo || "",
        estado: a.estado,
      });
    }).catch(() => alert("Error al cargar asignación"));
  }, [id]);

  const handleChange = (field: keyof AsignacionCreate, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        const payload: AsignacionUpdate = {};
        for (const [k, v] of Object.entries(form)) {
          if (v !== undefined && v !== "") (payload as Record<string, unknown>)[k] = v;
        }
        await asignacionesApi.actualizar(Number(id), payload);
      } else {
        await asignacionesApi.crear(form);
      }
      navigate("/asignaciones");
    } catch {
      alert("Error al guardar asignación");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Asignación" : "Nueva Asignación"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Activo ID" required>
          <input
            type="number"
            style={inputStyle}
            value={form.activo_id}
            onChange={(e) => handleChange("activo_id", Number(e.target.value))}
            required
          />
        </FormField>

        <FormField label="Usuario ID" required>
          <input
            type="number"
            style={inputStyle}
            value={form.usuario_id}
            onChange={(e) => handleChange("usuario_id", Number(e.target.value))}
            required
          />
        </FormField>

        <FormField label="Fecha Asignación" required>
          <input
            type="date"
            style={inputStyle}
            value={form.fecha_asignacion}
            onChange={(e) => handleChange("fecha_asignacion", e.target.value)}
            required
          />
        </FormField>

        <FormField label="Fecha Devolución">
          <input
            type="date"
            style={inputStyle}
            value={form.fecha_devolucion}
            onChange={(e) => handleChange("fecha_devolucion", e.target.value)}
          />
        </FormField>

        <FormField label="Motivo">
          <textarea
            style={inputStyle}
            value={form.motivo}
            onChange={(e) => handleChange("motivo", e.target.value)}
            rows={3}
          />
        </FormField>

        <FormField label="Estado" required>
          <select
            style={inputStyle}
            value={form.estado}
            onChange={(e) => handleChange("estado", e.target.value)}
            required
          >
            {ESTADOS.map((e) => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnPrimary}>Guardar</button>
          <button type="button" onClick={() => navigate("/asignaciones")} style={btnSecondary}>Cancelar</button>
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
  gap: "0.8rem",
  marginTop: "0.5rem",
};

const btnPrimary: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
};

const btnSecondary: React.CSSProperties = {
  background: "none",
  border: "1px solid var(--border)",
  color: "var(--text-secondary)",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
};
