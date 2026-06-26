import { useState, useEffect, type FormEvent, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { activosApi, type ActivoCreate, type ActivoUpdate, type ActivoFoto } from "../../api/activos.api";
import FormField from "../../components/common/FormField";
import Button from "../../components/common/Button";
import MapPicker from "../../components/MapPicker";
import CameraCapture from "../../components/CameraCapture";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft, Trash2 } from "lucide-react";

const ESTADOS = ["Disponible", "Asignado", "En Mantenimiento", "Inactivo", "Reservado", "Baja"];

export default function FormularioActivo() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);
  const [loading, setLoading] = useState(false);
  const [fotos, setFotos] = useState<ActivoFoto[]>([]);
  const [uploadingFoto, setUploadingFoto] = useState(false);

  const [form, setForm] = useState<ActivoCreate>({
    codigo: "",
    nombre: "",
    descripcion: "",
    categoria_id: 0,
    estado: "Disponible",
    numero_serie: "",
    valor_adquisicion: 0,
    fecha_adquisicion: "",
    ubicacion_actual: "",
    latitud: null,
    longitud: null,
  });

  const cargarFotos = useCallback(async (activoId: number) => {
    try {
      const res = await activosApi.listarFotos(activoId);
      setFotos(res.data);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => {
    if (!id) return;
    activosApi.obtener(Number(id)).then((res) => {
      const a = res.data;
      setForm({
        codigo: a.codigo,
        nombre: a.nombre,
        descripcion: a.descripcion || "",
        categoria_id: a.categoria_id,
        estado: a.estado,
        numero_serie: a.numero_serie || "",
        valor_adquisicion: a.valor_adquisicion ?? 0,
        fecha_adquisicion: a.fecha_adquisicion || "",
        ubicacion_actual: a.ubicacion_actual || "",
        latitud: a.latitud,
        longitud: a.longitud,
      });
      cargarFotos(Number(id));
    }).catch(() => alert("Error al cargar activo"));
  }, [id, cargarFotos]);

  const handleSubirFoto = async (file: File) => {
    if (!id) return;
    setUploadingFoto(true);
    try {
      await activosApi.subirFoto(Number(id), file);
      toast("Foto subida correctamente", "success");
      cargarFotos(Number(id));
    } catch {
      toast("Error al subir la foto", "error");
    } finally {
      setUploadingFoto(false);
    }
  };

  const handleEliminarFoto = async (foto: ActivoFoto) => {
    if (!id) return;
    try {
      await activosApi.eliminarFoto(Number(id), foto.id);
      setFotos((prev) => prev.filter((f) => f.id !== foto.id));
      toast("Foto eliminada", "success");
    } catch {
      toast("Error al eliminar la foto", "error");
    }
  };

  const handleChange = (field: keyof ActivoCreate, value: string | number) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const payload: ActivoUpdate = {};
        for (const [k, v] of Object.entries(form)) {
          if (v !== undefined && v !== "") (payload as Record<string, unknown>)[k] = v;
        }
        delete (payload as Record<string, unknown>).codigo;
        await activosApi.actualizar(Number(id), payload);
      } else {
        await activosApi.crear(form);
      }
      navigate("/activos");
    } catch {
      alert("Error al guardar activo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>{isEdit ? "Editar Activo" : "Nuevo Activo"}</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <FormField label="Código" required>
          <input style={inputStyle} value={form.codigo} onChange={(e) => handleChange("codigo", e.target.value)} required />
        </FormField>
        <FormField label="Nombre" required>
          <input style={inputStyle} value={form.nombre} onChange={(e) => handleChange("nombre", e.target.value)} required />
        </FormField>
        <FormField label="Descripción">
          <textarea style={inputStyle} value={form.descripcion} onChange={(e) => handleChange("descripcion", e.target.value)} rows={3} />
        </FormField>
        <FormField label="Categoría ID" required>
          <input type="number" style={inputStyle} value={form.categoria_id} onChange={(e) => handleChange("categoria_id", Number(e.target.value))} required />
        </FormField>
        <FormField label="Estado" required>
          <select style={inputStyle} value={form.estado} onChange={(e) => handleChange("estado", e.target.value)} required>
            {ESTADOS.map((e) => (<option key={e} value={e}>{e}</option>))}
          </select>
        </FormField>
        <FormField label="Número de Serie">
          <input style={inputStyle} value={form.numero_serie} onChange={(e) => handleChange("numero_serie", e.target.value)} />
        </FormField>
        <FormField label="Valor de Adquisición">
          <input type="number" style={inputStyle} value={form.valor_adquisicion} onChange={(e) => handleChange("valor_adquisicion", Number(e.target.value))} />
        </FormField>
        <FormField label="Fecha de Adquisición">
          <input type="date" style={inputStyle} value={form.fecha_adquisicion} onChange={(e) => handleChange("fecha_adquisicion", e.target.value)} />
        </FormField>
        <FormField label="Ubicación (mapa)">
          <div style={{ marginBottom: "var(--space-sm)", fontSize: "var(--font-size-sm)", color: "var(--text-muted)" }}>
            {form.latitud && form.longitud ? `${form.latitud.toFixed(4)}, ${form.longitud.toFixed(4)}` : "Haz clic en el mapa o arrastra el marcador"}
          </div>
          <MapPicker latitud={form.latitud ?? null} longitud={form.longitud ?? null} onChange={(lat, lng) => setForm((prev) => ({ ...prev, latitud: lat, longitud: lng }))} />
        </FormField>

        {isEdit && (
          <FormField label="Fotos">
            <div style={fotosGrid}>
              {fotos.map((foto) => (
                <div key={foto.id} style={fotoThumb}>
                  <img src={`http://localhost:8000/${foto.url}`} alt={`Foto ${foto.orden}`} style={thumbImg} />
                  <button type="button" style={deleteFotoBtn} onClick={() => handleEliminarFoto(foto)} title="Eliminar foto">
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
            <div style={{ marginTop: "0.5rem" }}>
              <CameraCapture onUpload={handleSubirFoto} uploading={uploadingFoto} />
            </div>
          </FormField>
        )}

        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/activos")}>Cancelar</Button>
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

const fotosGrid: React.CSSProperties = {
  display: "flex",
  gap: "0.5rem",
  flexWrap: "wrap",
};

const fotoThumb: React.CSSProperties = {
  position: "relative",
  width: 100,
  height: 100,
  borderRadius: "var(--radius-sm)",
  overflow: "hidden",
  border: "1px solid var(--border)",
};

const thumbImg: React.CSSProperties = {
  width: "100%",
  height: "100%",
  objectFit: "cover",
};

const deleteFotoBtn: React.CSSProperties = {
  position: "absolute",
  top: 4,
  right: 4,
  background: "rgba(0,0,0,0.6)",
  color: "#fff",
  border: "none",
  borderRadius: "50%",
  width: 24,
  height: 24,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  cursor: "pointer",
};

const actionsStyle: React.CSSProperties = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "0.5rem",
};
