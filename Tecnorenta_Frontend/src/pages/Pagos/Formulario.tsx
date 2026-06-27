import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { pagosApi } from "../../api/pagos.api";
import { contratosApi } from "../../api/contratos.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

interface PagoForm {
  id_contrato: number;
  concepto: string;
  monto: number;
  fecha: string;
  estado: string;
}

const estados = ["pendiente", "pagado", "atrasado", "rechazado", "anulado"];

export default function FormularioPago() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<PagoForm>({
    id_contrato: 0,
    concepto: "",
    monto: 0,
    fecha: "",
    estado: "pendiente",
  });

  useEffect(() => {
    if (!id) return;
    pagosApi.obtener(Number(id)).then((res) => {
      const p = res.data;
      setForm({
        id_contrato: p.id_contrato,
        concepto: p.concepto,
        monto: p.monto,
        fecha: p.fecha.slice(0, 10),
        estado: p.estado,
      });
    }).catch(() => toast("Error al cargar pago", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await pagosApi.actualizar(Number(id), { monto: form.monto, estado: form.estado, concepto: form.concepto, fecha: form.fecha });
        toast("Pago actualizado", "success");
      } else {
        await pagosApi.crear(form);
        toast("Pago creado", "success");
      }
      navigate("/pagos");
    } catch {
      toast("Error al guardar pago", "error");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Pago" : "Nuevo Pago"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información del Pago">
          <FormField label="Contrato" required>
            <SearchableSelect
              value={form.id_contrato || null}
              onChange={(v) => setForm({ ...form, id_contrato: v })}
              loadOptions={async () => {
                const res = await contratosApi.listar();
                return res.data.map((c: { id: number }) => ({ id: c.id, label: `Contrato #${c.id}` }));
              }}
              placeholder="Buscar contrato..."
            />
          </FormField>
          <FormField label="Concepto" required>
            <input style={inputStyle} value={form.concepto} onChange={(e) => setForm({ ...form, concepto: e.target.value })} required />
          </FormField>
          <FormField label="Monto" required>
            <input type="number" step="0.01" style={inputStyle} value={form.monto} onChange={(e) => setForm({ ...form, monto: Number(e.target.value) })} required />
          </FormField>
          <FormField label="Fecha Pago" required>
            <input type="date" style={inputStyle} value={form.fecha} onChange={(e) => setForm({ ...form, fecha: e.target.value })} required />
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })} required>
              {estados.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" icon={<Save size={16} />}>{isEdit ? "Actualizar" : "Guardar"}</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/pagos")}>Cancelar</Button>
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
