import { useState, useEffect, type FormEvent } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { asignacionesApi, type AsignacionCreate, type AsignacionUpdate } from "../../api/asignaciones.api";
import { activosApi } from "../../api/activos.api";
import { usuarioApi } from "../../api/usuario.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const ESTADOS = ["Activa", "Pendiente", "Devuelta", "Cancelada"];

export default function FormularioAsignacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
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
              value={form.activo_id || null}
              onChange={(v) => handleChange("activo_id", v)}
              loadOptions={async () => {
                const res = await activosApi.listar();
                return res.data.map((a) => ({ id: a.id, label: `${a.codigo_inventario} - ${a.modelo}` }));
              }}
              placeholder="Buscar activo..."
            />
          </FormField>
          <FormField label="Usuario" required>
            <SearchableSelect
              value={form.usuario_id || null}
              onChange={(v) => handleChange("usuario_id", v)}
              loadOptions={async () => {
                const res = await usuarioApi.listar();
                return res.data.map((u: { id: number; nombre: string }) => ({ id: u.id, label: u.nombre }));
              }}
              placeholder="Buscar usuario..."
            />
          </FormField>
          <FormField label="Fecha Asignación" required>
            <input type="date" style={inputStyle} value={form.fecha_asignacion} onChange={(e) => handleChange("fecha_asignacion", e.target.value)} required />
          </FormField>
          <FormField label="Fecha Devolución">
            <input type="date" style={inputStyle} value={form.fecha_devolucion} onChange={(e) => handleChange("fecha_devolucion", e.target.value)} />
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => handleChange("estado", e.target.value)} required>
              {ESTADOS.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
        </FormSection>
        <FormSection title="Detalles">
          <FormField label="Motivo">
            <textarea style={inputStyle} value={form.motivo} onChange={(e) => handleChange("motivo", e.target.value)} rows={3} />
          </FormField>
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
