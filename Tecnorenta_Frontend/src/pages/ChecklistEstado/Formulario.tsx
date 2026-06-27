import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { checklistEstadoApi, type ChecklistEstadoCreate, type ChecklistEstadoUpdate } from "../../api/checklist-estado.api";
import { asignacionesApi } from "../../api/asignaciones.api";
import { usuarioApi } from "../../api/usuario.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

const momentos = ["entrega", "devolucion"];
const estadosComponente = ["bien", "rayado", "roto"];

export default function FormularioChecklistEstado() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);
  const [idAsignacion, setIdAsignacion] = useState(0);
  const [momento, setMomento] = useState("entrega");
  const [pantalla, setPantalla] = useState("bien");
  const [teclado, setTeclado] = useState("bien");
  const [carcasa, setCarcasa] = useState("bien");
  const [cargador, setCargador] = useState(true);
  const [observaciones, setObservaciones] = useState("");
  const [urlFotos, setUrlFotos] = useState("");
  const [idUsuario, setIdUsuario] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    checklistEstadoApi.obtener(Number(id)).then((res) => {
      const c = res.data;
      setIdAsignacion(c.id_asignacion);
      setMomento(c.momento);
      setPantalla(c.pantalla);
      setTeclado(c.teclado);
      setCarcasa(c.carcasa);
      setCargador(c.cargador);
      setObservaciones(c.observaciones ?? "");
      setUrlFotos(c.url_fotos ?? "");
      setIdUsuario(c.id_usuario);
    }).catch(() => toast("Error al cargar el checklist", "error"));
  }, [id, toast]);

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
        toast("Checklist actualizado", "success");
      } else {
        const data: ChecklistEstadoCreate = {
          id_asignacion: idAsignacion, momento, pantalla, teclado, carcasa,
          cargador, id_usuario: idUsuario,
          observaciones: observaciones || undefined,
          url_fotos: urlFotos || undefined,
        };
        await checklistEstadoApi.crear(data);
        toast("Checklist creado", "success");
      }
      navigate("/checklist");
    } catch {
      toast(`Error al ${isEdit ? "actualizar" : "crear"} el checklist`, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Checklist" : "Nuevo Checklist"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Asignación">
          <FormField label="Asignación" required>
            <SearchableSelect
              value={idAsignacion || null}
              onChange={(v) => setIdAsignacion(v)}
              loadOptions={async () => {
                const res = await asignacionesApi.listar();
                return res.data.map((a) => ({ id: a.id, label: `#${a.id} - Activo ${a.id_activo}` }));
              }}
              placeholder="Buscar asignación..."
              disabled={isEdit}
            />
          </FormField>
          <FormField label="Usuario" required>
            <SearchableSelect
              value={idUsuario || null}
              onChange={(v) => setIdUsuario(v)}
              loadOptions={async () => {
                const res = await usuarioApi.listar();
                return res.data.map((u: { id: number; nombre: string }) => ({ id: u.id, label: u.nombre }));
              }}
              placeholder="Buscar usuario..."
              disabled={isEdit}
            />
          </FormField>
          <FormField label="Momento" required>
            <select style={inputStyle} value={momento} onChange={(e) => setMomento(e.target.value)} required>
              {momentos.map((m) => (<option key={m} value={m}>{m}</option>))}
            </select>
          </FormField>
        </FormSection>
        <FormSection title="Estado de Componentes">
          <FormField label="Pantalla" required>
            <select style={inputStyle} value={pantalla} onChange={(e) => setPantalla(e.target.value)} required>
              {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
          <FormField label="Teclado" required>
            <select style={inputStyle} value={teclado} onChange={(e) => setTeclado(e.target.value)} required>
              {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
          <FormField label="Carcasa" required>
            <select style={inputStyle} value={carcasa} onChange={(e) => setCarcasa(e.target.value)} required>
              {estadosComponente.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
          <FormField label="Cargador" required>
            <select style={inputStyle} value={String(cargador)} onChange={(e) => setCargador(e.target.value === "true")} required>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </FormField>
        </FormSection>
        <FormSection title="Observaciones">
          <div style={{ gridColumn: "1 / -1" }}>
            <FormField label="Observaciones">
              <textarea style={inputStyle} value={observaciones} onChange={(e) => setObservaciones(e.target.value)} rows={3} />
            </FormField>
            <FormField label="URL Fotos">
              <input style={inputStyle} value={urlFotos} onChange={(e) => setUrlFotos(e.target.value)} />
            </FormField>
          </div>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/checklist")}>Cancelar</Button>
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
