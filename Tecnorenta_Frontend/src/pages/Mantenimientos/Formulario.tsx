import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { mantenimientosApi, type MantenimientoCreate } from "../../api/mantenimientos.api";
import { activosApi } from "../../api/activos.api";
import { reportesApi } from "../../api/reportes.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioMantenimiento() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<MantenimientoCreate>({
    tipo: "preventivo",
    fecha: "",
    costo: 0,
    descripcion: "",
    id_activo: 0,
    frecuencia_dias: null,
    proxima_fecha: null,
    id_reporte_origen: null,
    tiempo_reparacion: null,
  });

  useEffect(() => {
    if (!id) return;
    mantenimientosApi.obtener(Number(id)).then((res) => {
      const m = res.data;
      setForm({
        tipo: m.tipo,
        fecha: m.fecha ? m.fecha.slice(0, 10) : "",
        costo: m.costo ?? 0,
        descripcion: m.descripcion ?? "",
        id_activo: m.id_activo,
        frecuencia_dias: m.frecuencia_dias,
        proxima_fecha: m.proxima_fecha ? m.proxima_fecha.slice(0, 10) : null,
        id_reporte_origen: m.id_reporte_origen,
        tiempo_reparacion: m.tiempo_reparacion,
      });
    }).catch(() => toast("Error al cargar mantenimiento", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.id_activo) {
      toast("Seleccione un activo", "error");
      return;
    }
    try {
      if (isEdit) {
        await mantenimientosApi.actualizar(Number(id), {
          costo: form.costo,
          descripcion: form.descripcion,
          proxima_fecha: form.proxima_fecha || null,
          tiempo_reparacion: form.tiempo_reparacion,
        });
        toast("Mantenimiento actualizado", "success");
      } else {
        await mantenimientosApi.crear({
          ...form,
          proxima_fecha: form.proxima_fecha || null,
          frecuencia_dias: form.frecuencia_dias || null,
          id_reporte_origen: form.id_reporte_origen || null,
          tiempo_reparacion: form.tiempo_reparacion || null,
        });
        toast("Mantenimiento creado", "success");
      }
      navigate("/mantenimientos");
    } catch {
      toast("Error al guardar mantenimiento", "error");
    }
  };

  const esPreventivo = form.tipo === "preventivo";

  return (
    <div>
      <h2>{isEdit ? "Editar Mantenimiento" : "Nuevo Mantenimiento"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información General">
          <FormField label="Activo" required>
            <SearchableSelect
              value={form.id_activo || null}
              onChange={(v) => setForm({ ...form, id_activo: v })}
              loadOptions={async () => {
                const items = await activosApi.listarTodos();
                return items.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Tipo" required>
            <select
              style={inputStyle}
              value={form.tipo}
              onChange={(e) => setForm({ ...form, tipo: e.target.value })}
              disabled={isEdit}
            >
              <option value="preventivo">Preventivo</option>
              <option value="correctivo">Correctivo</option>
            </select>
          </FormField>
          <FormField label="Fecha" required>
            <input type="date" style={inputStyle} value={form.fecha} onChange={(e) => setForm({ ...form, fecha: e.target.value })} required />
          </FormField>
          <FormField label="Costo (Bs)">
            <input type="number" step="0.01" min="0" style={inputStyle} value={form.costo} onChange={(e) => setForm({ ...form, costo: Number(e.target.value) })} />
          </FormField>
        </FormSection>

        {esPreventivo ? (
          <FormSection title="Plan preventivo">
            <FormField label="Frecuencia (días)">
              <input type="number" min="1" style={inputStyle} value={form.frecuencia_dias ?? ""} onChange={(e) => setForm({ ...form, frecuencia_dias: e.target.value ? Number(e.target.value) : null })} />
            </FormField>
            <FormField label="Próxima fecha">
              <input type="date" style={inputStyle} value={form.proxima_fecha ?? ""} onChange={(e) => setForm({ ...form, proxima_fecha: e.target.value || null })} />
            </FormField>
          </FormSection>
        ) : (
          <FormSection title="Datos del correctivo">
            <FormField label="Incidencia de origen">
              <SearchableSelect
                value={form.id_reporte_origen ?? null}
                onChange={(v) => setForm({ ...form, id_reporte_origen: v })}
                loadOptions={async () => {
                  const items = await reportesApi.listarTodos();
                  return items.map((r) => ({ id: r.id, label: `#${r.id} · ${r.descripcion.slice(0, 40)}` }));
                }}
                placeholder="Buscar incidencia..."
              />
            </FormField>
            <FormField label="Tiempo de reparación (días)">
              <input type="number" min="0" style={inputStyle} value={form.tiempo_reparacion ?? ""} onChange={(e) => setForm({ ...form, tiempo_reparacion: e.target.value ? Number(e.target.value) : null })} />
            </FormField>
          </FormSection>
        )}

        <FormSection title="Descripción">
          <div style={{ gridColumn: "1 / -1" }}>
            <FormField label="Descripción">
              <textarea style={inputStyle} value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} rows={4} />
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
