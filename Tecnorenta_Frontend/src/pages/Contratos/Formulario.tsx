import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { contratosApi, type ContratoCreate } from "../../api/contratos.api";
import FormField from "../../components/common/FormField";

const estados = ["Activo", "Pendiente", "Vencido", "Cancelado"];

export default function FormularioContrato() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
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
    });
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (isEdit) {
        await contratosApi.actualizar(Number(id), form);
      } else {
        await contratosApi.crear(form);
      }
      navigate("/contratos");
    } catch {
      alert("Error al guardar contrato");
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Contrato" : "Nuevo Contrato"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Cliente ID" required>
          <input
            type="number"
            value={form.cliente_id}
            onChange={(e) => setForm({ ...form, cliente_id: Number(e.target.value) })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Número de Contrato" required>
          <input
            value={form.numero_contrato}
            onChange={(e) => setForm({ ...form, numero_contrato: e.target.value })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Fecha Inicio" required>
          <input
            type="date"
            value={form.fecha_inicio}
            onChange={(e) => setForm({ ...form, fecha_inicio: e.target.value })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Fecha Fin" required>
          <input
            type="date"
            value={form.fecha_fin}
            onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Monto Total" required>
          <input
            type="number"
            step="0.01"
            value={form.monto_total}
            onChange={(e) => setForm({ ...form, monto_total: Number(e.target.value) })}
            required
            style={inputStyle}
          />
        </FormField>

        <FormField label="Estado" required>
          <select
            value={form.estado}
            onChange={(e) => setForm({ ...form, estado: e.target.value })}
            required
            style={inputStyle}
          >
            {estados.map((est) => (
              <option key={est} value={est}>
                {est}
              </option>
            ))}
          </select>
        </FormField>

        <div style={actionsStyle}>
          <button type="submit" style={btnPrimary}>
            {isEdit ? "Actualizar" : "Guardar"}
          </button>
          <button type="button" onClick={() => navigate("/contratos")} style={btnSecondary}>
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
