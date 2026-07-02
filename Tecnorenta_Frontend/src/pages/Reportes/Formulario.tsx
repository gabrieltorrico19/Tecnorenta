import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { reportesApi, type ReporteCreate, type ReporteUpdate } from "../../api/reportes.api";
import { activosApi } from "../../api/activos.api";
import { usuarioApi } from "../../api/usuario.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const TIPOS_INCIDENCIA = ["Daño Físico", "Fallo Técnico", "Software", "Pérdida", "Robo", "Otro"];
const ESTADOS = ["Reportada", "En Revisión", "Resuelta", "Cerrada"];

export default function FormularioReporte() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
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
    }).catch(() => toast("Error al cargar reporte", "error"));
  }, [id, toast]);

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
        toast("Reporte actualizado", "success");
      } else {
        await reportesApi.crear(form);
        toast("Reporte creado", "success");
      }
      navigate("/reportes");
    } catch {
      toast("Error al guardar reporte", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Reporte" : "Nuevo Reporte"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información del Reporte">
          <FormField label="Activo" required>
            <SearchableSelect
              value={form.activo_id || null}
              onChange={(v) => handleChange("activo_id", v)}
              loadOptions={async () => {
                const items = await activosApi.listarTodos();
                return items.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Usuario" required>
            <SearchableSelect
              value={form.usuario_id || null}
              onChange={(v) => handleChange("usuario_id", v)}
              loadOptions={async () => {
                const items = await usuarioApi.listarTodos();
                return items.map((u: { id: number; nombre: string }) => ({ id: u.id, label: u.nombre }));
              }}
              placeholder="Buscar usuario..."
            />
          </FormField>
          <FormField label="Tipo de Incidencia" required>
            <select style={inputStyle} value={form.tipo_incidencia} onChange={(e) => handleChange("tipo_incidencia", e.target.value)} required>
              {TIPOS_INCIDENCIA.map((t) => (<option key={t} value={t}>{t}</option>))}
            </select>
          </FormField>
          <FormField label="Fecha del Reporte" required>
            <input type="date" style={inputStyle} value={form.fecha_reporte} onChange={(e) => handleChange("fecha_reporte", e.target.value)} required />
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => handleChange("estado", e.target.value)} required>
              {ESTADOS.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
        </FormSection>
        <FormSection title="Descripción">
          <div style={{ gridColumn: "1 / -1" }}>
            <FormField label="Descripción" required>
              <textarea style={inputStyle} value={form.descripcion} onChange={(e) => handleChange("descripcion", e.target.value)} rows={4} required />
            </FormField>
          </div>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/reportes")}>Cancelar</Button>
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
