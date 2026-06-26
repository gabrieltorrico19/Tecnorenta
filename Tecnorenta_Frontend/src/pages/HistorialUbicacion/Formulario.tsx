import { type FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../../components/common/FormField";
import Button from "../../components/common/Button";
import { historialUbicacionApi, type HistorialUbicacionCreate, type HistorialUbicacionUpdate } from "../../api/historial-ubicacion.api";
import { Save, ArrowLeft } from "lucide-react";

export default function FormularioHistorialUbicacion() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [idAsignacion, setIdAsignacion] = useState("");
  const [latitud, setLatitud] = useState("");
  const [longitud, setLongitud] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    historialUbicacionApi.obtener(Number(id)).then((res) => {
      setIdAsignacion(String(res.data.id_asignacion));
      setLatitud(String(res.data.latitud));
      setLongitud(String(res.data.longitud));
    }).catch(() => alert("Error al cargar el registro"));
  }, [id]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const data: HistorialUbicacionUpdate = {
          latitud: latitud ? Number(latitud) : undefined,
          longitud: longitud ? Number(longitud) : undefined,
        };
        await historialUbicacionApi.actualizar(Number(id), data);
      } else {
        const data: HistorialUbicacionCreate = {
          id_asignacion: Number(idAsignacion),
          latitud: Number(latitud),
          longitud: Number(longitud),
        };
        await historialUbicacionApi.crear(data);
      }
      navigate("/historial-ubicacion");
    } catch {
      alert(`Error al ${isEdit ? "actualizar" : "crear"} el registro`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Registro de Ubicación" : "Nuevo Registro de Ubicación"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="ID Asignación" required>
          <input
            type="number"
            value={idAsignacion}
            onChange={(e) => setIdAsignacion(e.target.value)}
            required
            disabled={isEdit}
            style={inputStyle}
          />
        </FormField>
        <FormField label="Latitud" required>
          <input
            type="number"
            step="any"
            value={latitud}
            onChange={(e) => setLatitud(e.target.value)}
            required
            placeholder="-90 a 90"
            style={inputStyle}
          />
        </FormField>
        <FormField label="Longitud" required>
          <input
            type="number"
            step="any"
            value={longitud}
            onChange={(e) => setLongitud(e.target.value)}
            required
            placeholder="-180 a 180"
            style={inputStyle}
          />
        </FormField>
        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/historial-ubicacion")}>Cancelar</Button>
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
