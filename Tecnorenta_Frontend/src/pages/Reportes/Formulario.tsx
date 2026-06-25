import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { reportesApi, type ReporteCreate, type ReporteUpdate } from "../../api/reportes.api";
import FormField from "../../components/common/FormField";

const TIPOS_INCIDENCIA = ["Daño Físico", "Fallo Técnico", "Software", "Pérdida", "Robo", "Otro"];
const ESTADOS = ["Reportada", "En Revisión", "Resuelta", "Cerrada"];

export default function FormularioReporte() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<ReporteCreate>({
    activo_id: 0,
    usuario_id: 0,
    tipo_incidencia: "Daño Físico",
    descripcion: "",
    fecha_reporte: "",
    estado: "Reportada",
  });

  useEffect(() => {
    if (!id) return;
    reportesApi.obtener(Number(id)).then((res) => {
      const r = res.data;
      setForm({
        activo_id: r.activo_id,
        usuario_id: r.usuario_id,
        tipo_incidencia: r.tipo_incidencia,
        descripcion: r.descripcion,
        fecha_reporte: r.fecha_reporte,
        estado: r.estado,
      });
    }).catch(() => alert("Error al cargar reporte"));
  }, [id]);

  const handleChange = (field: keyof ReporteCreate, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        const payload: ReporteUpdate = {};
        for (const [k, v] of Object.entries(form)) {
          if (v !== undefined && v !== "") (payload as Record<string, unknown>)[k] = v;
        }
        await reportesApi.actualizar(Number(id), payload);
      } else {
        await reportesApi.crear(form);
      }
      navigate("/reportes");
    } catch {
      alert("Error al guardar reporte");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Reporte" : "Nuevo Reporte"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="ID del Activo" required>
          <input
            type="number"
            style={inputStyle}
            value={form.activo_id}
            onChange={(e) => handleChange("activo_id", Number(e.target.value))}
            required
          />
        </FormField>

        <FormField label="ID del Usuario" required>
          <input
            type="number"
            style={inputStyle}
            value={form.usuario_id}
            onChange={(e) => handleChange("usuario_id", Number(e.target.value))}
            required
          />
        </FormField>

        <FormField label="Tipo de Incidencia" required>
          <select
            style={inputStyle}
            value={form.tipo_incidencia}
            onChange={(e) => handleChange("tipo_incidencia", e.target.value)}
            required
          >
            {TIPOS_INCIDENCIA.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </FormField>

        <FormField label="Descripción" required>
          <textarea
            style={inputStyle}
            value={form.descripcion}
            onChange={(e) => handleChange("descripcion", e.target.value)}
            rows={4}
            required
          />
        </FormField>

        <FormField label="Fecha del Reporte" required>
          <input
            type="date"
            style={inputStyle}
            value={form.fecha_reporte}
            onChange={(e) => handleChange("fecha_reporte", e.target.value)}
            required
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
          <button type="button" onClick={() => navigate("/reportes")} style={btnSecondary}>Cancelar</button>
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
