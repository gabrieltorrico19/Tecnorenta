import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { asignacionesApi, type AsignacionCreate, type AsignacionUpdate } from "../../api/asignaciones.api";
import { activosApi } from "../../api/activos.api";
import { contratosApi } from "../../api/contratos.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import MapPicker from "../../components/MapPicker";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioAsignacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<AsignacionCreate>({
    id_activo: 0,
    id_contrato: 0,
    fecha_asignacion: "",
    fecha_devolucion: "",
    latitud: null,
    longitud: null,
  });

  useEffect(() => {
    if (!id) return;
    asignacionesApi.obtener(Number(id)).then((res) => {
      const a = res.data;
      setForm({
        id_activo: a.id_activo,
        id_contrato: a.id_contrato,
        fecha_asignacion: a.fecha_asignacion,
        fecha_devolucion: a.fecha_devolucion || "",
        latitud: a.latitud,
        longitud: a.longitud,
      });
    }).catch(() => toast("Error al cargar asignación", "error"));
  }, [id, toast]);

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
        toast("Asignación actualizada", "success");
      } else {
        await asignacionesApi.crear(form);
        toast("Asignación creada", "success");
      }
      navigate("/asignaciones");
    } catch {
      toast("Error al guardar asignación", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Asignación" : "Nueva Asignación"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Asignación">
          <FormField label="Activo" required>
            <SearchableSelect
              value={form.id_activo || null}
              onChange={(v) => handleChange("id_activo", v)}
              loadOptions={async () => {
                const res = await activosApi.listar();
                return res.data.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Contrato" required>
            <SearchableSelect
              value={form.id_contrato || null}
              onChange={(v) => handleChange("id_contrato", v)}
              loadOptions={async () => {
                const res = await contratosApi.listar();
                return res.data.map((c: { id: number }) => ({ id: c.id, label: `Contrato #${c.id}` }));
              }}
              placeholder="Buscar contrato..."
            />
          </FormField>
          <FormField label="Fecha Asignación" required>
            <input type="date" style={inputStyle} value={form.fecha_asignacion} onChange={(e) => handleChange("fecha_asignacion", e.target.value)} required />
          </FormField>
          <FormField label="Fecha Devolución">
            <input type="date" style={inputStyle} value={form.fecha_devolucion} onChange={(e) => handleChange("fecha_devolucion", e.target.value)} />
          </FormField>
        </FormSection>
        <FormSection title="Ubicación">
          <div style={{ gridColumn: "1 / -1" }}>
            <div style={{ marginBottom: "var(--space-sm)", fontSize: "var(--font-size-sm)", color: "var(--text-muted)" }}>
              {form.latitud && form.longitud ? `${form.latitud.toFixed(4)}, ${form.longitud.toFixed(4)}` : "Haz clic en el mapa o arrastra el marcador"}
            </div>
            <MapPicker latitud={form.latitud ?? null} longitud={form.longitud ?? null} onChange={(lat, lng) => setForm((prev) => ({ ...prev, latitud: lat, longitud: lng }))} />
          </div>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/asignaciones")}>Cancelar</Button>
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
