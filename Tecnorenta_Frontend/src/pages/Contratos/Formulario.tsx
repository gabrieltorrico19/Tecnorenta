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

const estados = ["Activo", "Pendiente", "Vencido", "Cancelado"];

export default function FormularioContrato() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<ContratoCreate>({
    cliente_id: 0,
    numero_contrato: "",
    fecha_inicio: "",
    fecha_fin: "",
    monto_total: 0,
    estado: "Pendiente",
  });

  useEffect(() => {
    if (!id) return;
    contratosApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setForm({
        cliente_id: c.cliente_id,
        numero_contrato: c.numero_contrato,
        fecha_inicio: c.fecha_inicio.slice(0, 10),
        fecha_fin: c.fecha_fin.slice(0, 10),
        monto_total: c.monto_total,
        estado: c.estado,
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
              value={form.cliente_id || null}
              onChange={(v) => setForm({ ...form, cliente_id: v })}
              loadOptions={async () => {
                const res = await clientesApi.listar();
                return res.data.map((c) => ({ id: c.id, label: c.nombre }));
              }}
              placeholder="Buscar cliente..."
            />
          </FormField>
          <FormField label="Número de Contrato" required>
            <input style={inputStyle} value={form.numero_contrato} onChange={(e) => setForm({ ...form, numero_contrato: e.target.value })} required />
          </FormField>
          <FormField label="Fecha Inicio" required>
            <input type="date" style={inputStyle} value={form.fecha_inicio} onChange={(e) => setForm({ ...form, fecha_inicio: e.target.value })} required />
          </FormField>
          <FormField label="Fecha Fin" required>
            <input type="date" style={inputStyle} value={form.fecha_fin} onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })} required />
          </FormField>
          <FormField label="Monto Total" required>
            <input type="number" step="0.01" style={inputStyle} value={form.monto_total} onChange={(e) => setForm({ ...form, monto_total: Number(e.target.value) })} required />
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
