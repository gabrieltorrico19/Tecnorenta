import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { reportesApi, type ReporteCreate, type ReporteUpdate } from "../../api/reportes.api";
import { activosApi } from "../../api/activos.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const GRAVEDADES = [
  { value: "leve", label: "Leve" },
  { value: "moderado", label: "Moderado" },
  { value: "grave", label: "Grave" },
];
const ESTADOS = [
  { value: "abierto", label: "Abierto" },
  { value: "en_atencion", label: "En atención" },
  { value: "cerrado", label: "Cerrado" },
];

export default function FormularioReporte() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<ReporteCreate>({
    fecha: "",
    descripcion: "",
    gravedad: "leve",
    estado: "abierto",
    id_activo: 0,
    url_foto: "",
  });

  useEffect(() => {
    if (!id) return;
    reportesApi.obtener(Number(id)).then((res) => {
      const r = res.data;
      setForm({
        fecha: r.fecha ? r.fecha.slice(0, 10) : "",
        descripcion: r.descripcion,
        gravedad: r.gravedad,
        estado: r.estado,
        id_activo: r.id_activo,
        url_foto: r.url_foto ?? "",
      });
    }).catch(() => toast("Error al cargar reporte", "error"));
  }, [id, toast]);

  const handleChange = (field: keyof ReporteCreate, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.id_activo) {
      toast("Seleccione un activo", "error");
      return;
    }
    try {
      if (isEdit) {
        const payload: ReporteUpdate = {
          descripcion: form.descripcion,
          gravedad: form.gravedad,
          estado: form.estado,
          url_foto: form.url_foto || undefined,
        };
        await reportesApi.actualizar(Number(id), payload);
        toast("Reporte actualizado", "success");
      } else {
        await reportesApi.crear({ ...form, url_foto: form.url_foto || undefined });
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
              value={form.id_activo || null}
              onChange={(v) => handleChange("id_activo", v)}
              loadOptions={async () => {
                const items = await activosApi.listarTodos();
                return items.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Fecha" required>
            <input type="date" style={inputStyle} value={form.fecha} onChange={(e) => handleChange("fecha", e.target.value)} required />
          </FormField>
          <FormField label="Gravedad" required>
            <select style={inputStyle} value={form.gravedad} onChange={(e) => handleChange("gravedad", e.target.value)} required>
              {GRAVEDADES.map((g) => (<option key={g.value} value={g.value}>{g.label}</option>))}
            </select>
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => handleChange("estado", e.target.value)} required>
              {ESTADOS.map((es) => (<option key={es.value} value={es.value}>{es.label}</option>))}
            </select>
          </FormField>
          <FormField label="URL de foto">
            <input type="url" style={inputStyle} value={form.url_foto} onChange={(e) => handleChange("url_foto", e.target.value)} placeholder="https://…" />
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
