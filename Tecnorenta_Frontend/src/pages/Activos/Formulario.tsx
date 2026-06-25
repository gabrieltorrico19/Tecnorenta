import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { activosApi, type ActivoCreate, type ActivoUpdate } from "../../api/activos.api";
import FormField from "../../components/common/FormField";

const ESTADOS = ["Disponible", "Asignado", "En Mantenimiento", "Inactivo", "Reservado", "Baja"];

export default function FormularioActivo() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<ActivoCreate>({
    codigo: "",
    nombre: "",
    descripcion: "",
    categoria_id: 0,
    estado: "Disponible",
    numero_serie: "",
    valor_adquisicion: 0,
    fecha_adquisicion: "",
    ubicacion_actual: "",
  });

  useEffect(() => {
    if (!id) return;
    activosApi.obtener(Number(id)).then((res) => {
      const a = res.data;
      setForm({
        codigo: a.codigo,
        nombre: a.nombre,
        descripcion: a.descripcion || "",
        categoria_id: a.categoria_id,
        estado: a.estado,
        numero_serie: a.numero_serie || "",
        valor_adquisicion: a.valor_adquisicion ?? 0,
        fecha_adquisicion: a.fecha_adquisicion || "",
        ubicacion_actual: a.ubicacion_actual || "",
      });
    }).catch(() => alert("Error al cargar activo"));
  }, [id]);

  const handleChange = (field: keyof ActivoCreate, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        const payload: ActivoUpdate = {};
        for (const [k, v] of Object.entries(form)) {
          if (v !== undefined && v !== "") (payload as Record<string, unknown>)[k] = v;
        }
        delete (payload as Record<string, unknown>).codigo;
        await activosApi.actualizar(Number(id), payload);
      } else {
        await activosApi.crear(form);
      }
      navigate("/activos");
    } catch {
      alert("Error al guardar activo");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Activo" : "Nuevo Activo"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Código" required>
          <input
            style={inputStyle}
            value={form.codigo}
            onChange={(e) => handleChange("codigo", e.target.value)}
            required
          />
        </FormField>

        <FormField label="Nombre" required>
          <input
            style={inputStyle}
            value={form.nombre}
            onChange={(e) => handleChange("nombre", e.target.value)}
            required
          />
        </FormField>

        <FormField label="Descripción">
          <textarea
            style={inputStyle}
            value={form.descripcion}
            onChange={(e) => handleChange("descripcion", e.target.value)}
            rows={3}
          />
        </FormField>

        <FormField label="Categoría ID" required>
          <input
            type="number"
            style={inputStyle}
            value={form.categoria_id}
            onChange={(e) => handleChange("categoria_id", Number(e.target.value))}
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

        <FormField label="Número de Serie">
          <input
            style={inputStyle}
            value={form.numero_serie}
            onChange={(e) => handleChange("numero_serie", e.target.value)}
          />
        </FormField>

        <FormField label="Valor de Adquisición">
          <input
            type="number"
            style={inputStyle}
            value={form.valor_adquisicion}
            onChange={(e) => handleChange("valor_adquisicion", Number(e.target.value))}
          />
        </FormField>

        <FormField label="Fecha de Adquisición">
          <input
            type="date"
            style={inputStyle}
            value={form.fecha_adquisicion}
            onChange={(e) => handleChange("fecha_adquisicion", e.target.value)}
          />
        </FormField>

        <FormField label="Ubicación Actual">
          <input
            style={inputStyle}
            value={form.ubicacion_actual}
            onChange={(e) => handleChange("ubicacion_actual", e.target.value)}
          />
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnPrimary}>Guardar</button>
          <button type="button" onClick={() => navigate("/activos")} style={btnSecondary}>Cancelar</button>
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
