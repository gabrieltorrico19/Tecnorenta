import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { contratosApi, type ContratoCreate } from "../../api/contratos.api";
import { clientesApi } from "../../api/clientes.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const estados = ["activo", "vencido", "cancelado", "renovado"];

export default function FormularioContrato() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<ContratoCreate>({
    id_cliente: 0,
    fecha_inicio: "",
    fecha_fin: "",
    monto_mensual: 0,
    estado: "activo",
    condiciones_uso: "",
  });

  useEffect(() => {
    if (!id) return;
    contratosApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setForm({
        id_cliente: c.id_cliente,
        fecha_inicio: c.fecha_inicio.slice(0, 10),
        fecha_fin: c.fecha_fin.slice(0, 10),
        monto_mensual: c.monto_mensual,
        estado: c.estado,
        condiciones_uso: c.condiciones_uso || "",
      });
    }).catch(() => toast("Error al cargar contrato", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await contratosApi.actualizar(Number(id), form);
        toast("Contrato actualizado", "success");
      } else {
        await contratosApi.crear(form);
        toast("Contrato creado", "success");
      }
      navigate("/contratos");
    } catch {
      toast("Error al guardar contrato", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Contrato" : "Nuevo Contrato"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información del Contrato">
          <FormField label="Cliente" required>
            <SearchableSelect
              value={form.id_cliente || null}
              onChange={(v) => setForm({ ...form, id_cliente: v })}
              loadOptions={async () => {
                const res = await clientesApi.listar();
                return res.data.map((c: { id: number; nombre: string }) => ({ id: c.id, label: c.nombre }));
              }}
              placeholder="Buscar cliente..."
            />
          </FormField>
          <FormField label="Fecha Inicio" required>
            <input type="date" style={inputStyle} value={form.fecha_inicio} onChange={(e) => setForm({ ...form, fecha_inicio: e.target.value })} required />
          </FormField>
          <FormField label="Fecha Fin" required>
            <input type="date" style={inputStyle} value={form.fecha_fin} onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })} required />
          </FormField>
          <FormField label="Monto Mensual" required>
            <input type="number" step="0.01" style={inputStyle} value={form.monto_mensual} onChange={(e) => setForm({ ...form, monto_mensual: Number(e.target.value) })} required />
          </FormField>
          <FormField label="Condiciones de Uso">
            <textarea style={inputStyle} value={form.condiciones_uso} onChange={(e) => setForm({ ...form, condiciones_uso: e.target.value })} rows={3} />
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })} required>
              {estados.map((est) => (<option key={est} value={est}>{est}</option>))}
            </select>
          </FormField>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>{isEdit ? "Actualizar" : "Guardar"}</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/contratos")}>Cancelar</Button>
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
