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
  contrato_id: number;
  monto: number;
  fecha_pago: string;
  metodo_pago: string;
  estado: string;
}

const metodosPago = ["Efectivo", "Transferencia", "Tarjeta Crédito", "Tarjeta Débito", "Cheque"];
const estados = ["Pendiente", "Pagado", "Atrasado", "Rechazado", "Anulado"];

export default function FormularioPago() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);

  const [form, setForm] = useState<PagoForm>({
    contrato_id: 0,
    monto: 0,
    fecha_pago: "",
    metodo_pago: "Efectivo",
    estado: "Pendiente",
  });

  useEffect(() => {
    if (!id) return;
    pagosApi.obtener(Number(id)).then((res) => {
      const p = res.data;
      setForm({
        contrato_id: p.contrato_id,
        monto: p.monto,
        fecha_pago: p.fecha_pago.slice(0, 10),
        metodo_pago: p.metodo_pago,
        estado: p.estado,
      });
    }).catch(() => toast("Error al cargar pago", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await pagosApi.actualizar(Number(id), { monto: form.monto, metodo_pago: form.metodo_pago, estado: form.estado });
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
              value={form.contrato_id || null}
              onChange={(v) => setForm({ ...form, contrato_id: v })}
              loadOptions={async () => {
                const res = await contratosApi.listar();
                return res.data.map((c) => ({ id: c.id, label: c.numero_contrato }));
              }}
              placeholder="Buscar contrato..."
            />
          </FormField>
          <FormField label="Monto" required>
            <input type="number" step="0.01" style={inputStyle} value={form.monto} onChange={(e) => setForm({ ...form, monto: Number(e.target.value) })} required />
          </FormField>
          <FormField label="Fecha Pago" required>
            <input type="date" style={inputStyle} value={form.fecha_pago} onChange={(e) => setForm({ ...form, fecha_pago: e.target.value })} required />
          </FormField>
          <FormField label="Método Pago" required>
            <select style={inputStyle} value={form.metodo_pago} onChange={(e) => setForm({ ...form, metodo_pago: e.target.value })} required>
              {metodosPago.map((m) => (<option key={m} value={m}>{m}</option>))}
            </select>
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
