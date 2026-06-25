import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { mantenimientosApi, type MantenimientoCreate } from "../../api/mantenimientos.api";
import FormField from "../../components/common/FormField";

const tipoOpciones = ["Preventivo", "Correctivo", "Predictivo", "Emergencia"];
const estadoOpciones = ["Pendiente", "En Progreso", "Completado", "Cancelado"];

export default function FormularioMantenimiento() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<MantenimientoCreate>({
    activo_id: 0,
    tipo_mantenimiento: "Preventivo",
    descripcion: "",
    fecha_inicio: "",
    fecha_fin: "",
    costo: 0,
    proveedor: "",
    estado: "Pendiente",
  });

  useEffect(() => {
    if (!id) return;
    mantenimientosApi.obtener(Number(id)).then((res) => {
      const m = res.data;
      setForm({
        activo_id: m.activo_id,
        tipo_mantenimiento: m.tipo_mantenimiento,
        descripcion: m.descripcion,
        fecha_inicio: m.fecha_inicio ? m.fecha_inicio.slice(0, 10) : "",
        fecha_fin: m.fecha_fin ? m.fecha_fin.slice(0, 10) : "",
        costo: m.costo ?? 0,
        proveedor: m.proveedor ?? "",
        estado: m.estado,
      });
    });
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await mantenimientosApi.actualizar(Number(id), form);
      } else {
        await mantenimientosApi.crear(form);
      }
      navigate("/mantenimientos");
    } catch {
      alert("Error al guardar mantenimiento");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Mantenimiento" : "Nuevo Mantenimiento"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Activo ID" required>
          <input
            type="number"
            value={form.activo_id}
            onChange={(e) => setForm({ ...form, activo_id: Number(e.target.value) })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Tipo de Mantenimiento">
          <select
            value={form.tipo_mantenimiento}
            onChange={(e) => setForm({ ...form, tipo_mantenimiento: e.target.value })}
            style={inputStyle}
          >
            {tipoOpciones.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="Descripción" required>
          <textarea
            value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
            required
            rows={4}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Fecha Inicio">
          <input
            type="date"
            value={form.fecha_inicio}
            onChange={(e) => setForm({ ...form, fecha_inicio: e.target.value })}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Fecha Fin">
          <input
            type="date"
            value={form.fecha_fin}
            onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Costo">
          <input
            type="number"
            step="0.01"
            value={form.costo}
            onChange={(e) => setForm({ ...form, costo: Number(e.target.value) })}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Proveedor">
          <input
            type="text"
            value={form.proveedor}
            onChange={(e) => setForm({ ...form, proveedor: e.target.value })}
            style={inputStyle}
          />
        </FormField>

        <FormField label="Estado">
          <select
            value={form.estado}
            onChange={(e) => setForm({ ...form, estado: e.target.value })}
            style={inputStyle}
          >
            {estadoOpciones.map((est) => (
              <option key={est} value={est}>
                {est}
              </option>
            ))}
          </select>
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnPrimary}>
            {isEdit ? "Actualizar" : "Guardar"}
          </button>
          <button type="button" onClick={() => navigate("/mantenimientos")} style={btnSecondary}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "0.8rem",
  maxWidth: "400px",
  marginTop: "1rem",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid #ccc",
  borderRadius: "4px",
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
  background: "transparent",
  color: "var(--text-secondary)",
  border: "1px solid var(--border)",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
};
