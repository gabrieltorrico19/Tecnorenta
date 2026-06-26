import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import { historialUbicacionApi, type HistorialUbicacionCreate, type HistorialUbicacionUpdate } from "../../api/historial-ubicacion.api";
import { asignacionesApi } from "../../api/asignaciones.api";
import MapPicker from "../../components/MapPicker";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioHistorialUbicacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);
  const [idAsignacion, setIdAsignacion] = useState(0);
  const [latitud, setLatitud] = useState<number | null>(null);
  const [longitud, setLongitud] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    historialUbicacionApi.obtener(Number(id)).then((res) => {
      setIdAsignacion(res.data.id_asignacion);
      setLatitud(res.data.latitud);
      setLongitud(res.data.longitud);
    }).catch(() => toast("Error al cargar el registro", "error"));
  }, [id, toast]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const data: HistorialUbicacionUpdate = {
          latitud: latitud ?? undefined,
          longitud: longitud ?? undefined,
        };
        await historialUbicacionApi.actualizar(Number(id), data);
        toast("Registro actualizado", "success");
      } else {
        const data: HistorialUbicacionCreate = {
          id_asignacion: idAsignacion,
          latitud: latitud ?? 0,
          longitud: longitud ?? 0,
        };
        await historialUbicacionApi.crear(data);
        toast("Registro creado", "success");
      }
      navigate("/historial-ubicacion");
    } catch {
      toast(`Error al ${isEdit ? "actualizar" : "crear"} el registro`, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Registro de Ubicación" : "Nuevo Registro de Ubicación"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Asignación">
          <FormField label="Asignación" required>
            <SearchableSelect
              value={idAsignacion || null}
              onChange={(v) => setIdAsignacion(v)}
              loadOptions={async () => {
                const res = await asignacionesApi.listar();
                return res.data.map((a) => ({ id: a.id, label: `#${a.id} - Activo ${a.activo_id}` }));
              }}
              placeholder="Buscar asignación..."
              disabled={isEdit}
            />
          </FormField>
        </FormSection>
        <FormSection title="Ubicación">
          <div style={{ gridColumn: "1 / -1" }}>
            <div style={{ marginBottom: "var(--space-sm)", fontSize: "var(--font-size-sm)", color: "var(--text-muted)" }}>
              {latitud && longitud ? `${latitud.toFixed(4)}, ${longitud.toFixed(4)}` : "Haz clic en el mapa o arrastra el marcador"}
            </div>
            <MapPicker latitud={latitud} longitud={longitud} onChange={(lat, lng) => { setLatitud(lat); setLongitud(lng); }} />
          </div>
        </FormSection>
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/historial-ubicacion")}>Cancelar</Button>
        </div>
      </form>
    </div>
  );
}

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "var(--space-lg)",
};
