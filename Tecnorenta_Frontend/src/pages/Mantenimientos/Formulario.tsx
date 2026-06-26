import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { mantenimientosApi, type MantenimientoCreate } from "../../api/mantenimientos.api";
import { activosApi } from "../../api/activos.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const tipoOpciones = ["Preventivo", "Correctivo", "Predictivo", "Emergencia"];
const estadoOpciones = ["Pendiente", "En Progreso", "Completado", "Cancelado"];

export default function FormularioMantenimiento() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
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
    }).catch(() => toast("Error al cargar mantenimiento", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await mantenimientosApi.actualizar(Number(id), form);
        toast("Mantenimiento actualizado", "success");
      } else {
        await mantenimientosApi.crear(form);
        toast("Mantenimiento creado", "success");
      }
      navigate("/mantenimientos");
    } catch {
      toast("Error al guardar mantenimiento", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Mantenimiento" : "Nuevo Mantenimiento"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información General">
          <FormField label="Activo" required>
            <SearchableSelect
              value={form.activo_id || null}
              onChange={(v) => setForm({ ...form, activo_id: v })}
              loadOptions={async () => {
                const res = await activosApi.listar();
                return res.data.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Tipo de Mantenimiento">
            <select style={inputStyle} value={form.tipo_mantenimiento} onChange={(e) => setForm({ ...form, tipo_mantenimiento: e.target.value })}>
              {tipoOpciones.map((t) => (<option key={t} value={t}>{t}</option>))}
            </select>
          </FormField>
          <FormField label="Estado">
            <select style={inputStyle} value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })}>
              {estadoOpciones.map((est) => (<option key={est} value={est}>{est}</option>))}
            </select>
          </FormField>
          <FormField label="Proveedor">
            <input style={inputStyle} value={form.proveedor} onChange={(e) => setForm({ ...form, proveedor: e.target.value })} />
          </FormField>
        </FormSection>
        <FormSection title="Fechas y Costos">
          <FormField label="Fecha Inicio">
            <input type="date" style={inputStyle} value={form.fecha_inicio} onChange={(e) => setForm({ ...form, fecha_inicio: e.target.value })} />
          </FormField>
          <FormField label="Fecha Fin">
            <input type="date" style={inputStyle} value={form.fecha_fin} onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })} />
          </FormField>
          <FormField label="Costo">
            <input type="number" step="0.01" style={inputStyle} value={form.costo} onChange={(e) => setForm({ ...form, costo: Number(e.target.value) })} />
          </FormField>
        </FormSection>
        <FormSection title="Descripción">
          <div style={{ gridColumn: "1 / -1" }}>
            <FormField label="Descripción" required>
              <textarea style={inputStyle} value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} required rows={4} />
            </FormField>
          </div>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>{isEdit ? "Actualizar" : "Guardar"}</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/mantenimientos")}>Cancelar</Button>
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
