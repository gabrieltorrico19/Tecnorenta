import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { pagosApi } from "../../api/pagos.api";
import FormField from "../../components/common/FormField";

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
    });
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await pagosApi.actualizar(Number(id), {
          monto: form.monto,
          metodo_pago: form.metodo_pago,
          estado: form.estado,
        });
      } else {
        await pagosApi.crear({
          contrato_id: form.contrato_id,
          monto: form.monto,
          fecha_pago: form.fecha_pago,
          metodo_pago: form.metodo_pago,
          estado: form.estado,
        });
      }
      navigate("/pagos");
    } catch {
      alert("Error al guardar pago");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Pago" : "Nuevo Pago"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Contrato ID" required>
          <input
            type="number"
            value={form.contrato_id}
            onChange={(e) => setForm({ ...form, contrato_id: Number(e.target.value) })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Monto" required>
          <input
            type="number"
            step="0.01"
            value={form.monto}
            onChange={(e) => setForm({ ...form, monto: Number(e.target.value) })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Fecha Pago" required>
          <input
            type="date"
            value={form.fecha_pago}
            onChange={(e) => setForm({ ...form, fecha_pago: e.target.value })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Método Pago" required>
          <select
            value={form.metodo_pago}
            onChange={(e) => setForm({ ...form, metodo_pago: e.target.value })}
            required
            style={inputStyle}
          >
            {metodosPago.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="Estado" required>
          <select
            value={form.estado}
            onChange={(e) => setForm({ ...form, estado: e.target.value })}
            required
            style={inputStyle}
          >
            {estados.map((e) => (
              <option key={e} value={e}>
                {e}
              </option>
            ))}
          </select>
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnPrimary}>
            {isEdit ? "Actualizar" : "Guardar"}
          </button>
          <button type="button" onClick={() => navigate("/pagos")} style={btnSecondary}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "0.8rem",
  maxWidth: "400px",
  marginTop: "1rem",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid #ccc",
  borderRadius: "4px",
  fontSize: "0.9rem",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.8rem",
  marginTop: "0.5rem",
};

const btnPrimary: React.CSSProperties = {
  background: "var(--accent)",
  color: "#fff",
  border: "none",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontWeight: 600,
};

const btnSecondary: React.CSSProperties = {
  background: "transparent",
  color: "var(--text-secondary)",
  border: "1px solid var(--border)",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
};
