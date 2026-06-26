import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import Button from "../../components/common/Button";
import { checklistEstadoApi, type ChecklistEstadoCreate, type ChecklistEstadoUpdate } from "../../api/checklist-estado.api";
import { Save, ArrowLeft } from "lucide-react";

const momentos = ["entrega", "devolucion"];
const estadosComponente = ["bien", "rayado", "roto"];

export default function FormularioChecklistEstado() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [idAsignacion, setIdAsignacion] = useState("");
  const [momento, setMomento] = useState("entrega");
  const [pantalla, setPantalla] = useState("bien");
  const [teclado, setTeclado] = useState("bien");
  const [carcasa, setCarcasa] = useState("bien");
  const [cargador, setCargador] = useState(true);
  const [observaciones, setObservaciones] = useState("");
  const [urlFotos, setUrlFotos] = useState("");
  const [idUsuario, setIdUsuario] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    checklistEstadoApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setIdAsignacion(String(c.id_asignacion));
      setMomento(c.momento);
      setPantalla(c.pantalla);
      setTeclado(c.teclado);
      setCarcasa(c.carcasa);
      setCargador(c.cargador);
      setObservaciones(c.observaciones ?? "");
      setUrlFotos(c.url_fotos ?? "");
      setIdUsuario(String(c.id_usuario));
    }).catch(() => alert("Error al cargar el checklist"));
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const data: ChecklistEstadoUpdate = {
          momento, pantalla, teclado, carcasa,
          cargador: cargador || undefined,
          observaciones: observaciones || undefined,
          url_fotos: urlFotos || undefined,
        };
        await checklistEstadoApi.actualizar(Number(id), data);
      } else {
        const data: ChecklistEstadoCreate = {
          id_asignacion: Number(idAsignacion),
          momento, pantalla, teclado, carcasa,
          cargador,
          observaciones: observaciones || undefined,
          url_fotos: urlFotos || undefined,
          id_usuario: Number(idUsuario),
        };
        await checklistEstadoApi.crear(data);
      }
      navigate("/checklist");
    } catch {
      alert(`Error al ${isEdit ? "actualizar" : "crear"} el checklist`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Checklist" : "Nuevo Checklist"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="ID Asignación" required>
          <input type="number" value={idAsignacion} onChange={(e) => setIdAsignacion(e.target.value)} required disabled={isEdit} style={inputStyle} />
        </FormField>
        <FormField label="Momento" required>
          <select value={momento} onChange={(e) => setMomento(e.target.value)} required style={inputStyle}>
            {momentos.map((m) => (<option key={m} value={m}>{m}</option>))}
          </select>
        </FormField>
        <FormField label="ID Usuario" required>
          <input type="number" value={idUsuario} onChange={(e) => setIdUsuario(e.target.value)} required disabled={isEdit} style={inputStyle} />
        </FormField>
        <FormField label="Pantalla" required>
          <select value={pantalla} onChange={(e) => setPantalla(e.target.value)} required style={inputStyle}>
            {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
          </select>
        </FormField>
        <FormField label="Teclado" required>
          <select value={teclado} onChange={(e) => setTeclado(e.target.value)} required style={inputStyle}>
            {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
          </select>
        </FormField>
        <FormField label="Carcasa" required>
          <select value={carcasa} onChange={(e) => setCarcasa(e.target.value)} required style={inputStyle}>
            {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
          </select>
        </FormField>
        <FormField label="Cargador" required>
          <select value={String(cargador)} onChange={(e) => setCargador(e.target.value === "true")} required style={inputStyle}>
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
        </FormField>
        <FormField label="Observaciones">
          <textarea value={observaciones} onChange={(e) => setObservaciones(e.target.value)} style={{ ...inputStyle, minHeight: 80, resize: "vertical" }} />
        </FormField>
        <FormField label="URL Fotos">
          <input value={urlFotos} onChange={(e) => setUrlFotos(e.target.value)} style={inputStyle} />
        </FormField>
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/checklist")}>Cancelar</Button>
        </div>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "var(--space-md)",
  maxWidth: "500px",
  marginTop: "var(--space-md)",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "var(--font-size-md)",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "0.5rem",
};
