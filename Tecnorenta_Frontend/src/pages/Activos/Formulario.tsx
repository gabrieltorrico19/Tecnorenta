import { useState, useEffect, type FormEvent, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { activosApi, type ActivoCreate, type ActivoUpdate, type ActivoFoto } from "../../api/activos.api";
import { categoriasApi } from "../../api/categorias.api";
import FormField from "../../components/common/FormField";
import FormSection from "../../components/common/FormSection";
import Button from "../../components/common/Button";
import SearchableSelect from "../../components/common/SearchableSelect";
import MapPicker from "../../components/MapPicker";
import CameraCapture from "../../components/CameraCapture";
import { useToast } from "../../context/ToastContext";
import { Save, ArrowLeft, Trash2 } from "lucide-react";

const ESTADOS = ["disponible", "rentado", "mantenimiento", "baja"];

export default function FormularioActivo() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEdit = Boolean(id);
  const [loading, setLoading] = useState(false);
  const [fotos, setFotos] = useState<ActivoFoto[]>([]);
  const [uploadingFoto, setUploadingFoto] = useState(false);

  const [form, setForm] = useState<ActivoCreate>({
    codigo_inventario: "",
    modelo: "",
    numero_serie: "",
    estado: "disponible",
    fecha_compra: null,
    valor_depreciado: 0,
    id_categoria: null,
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
        codigo_inventario: a.codigo_inventario,
        modelo: a.modelo,
        numero_serie: a.numero_serie,
        estado: a.estado,
        fecha_compra: a.fecha_compra,
        valor_depreciado: a.valor_depreciado,
        id_categoria: a.id_categoria,
        latitud: a.latitud,
        longitud: a.longitud,
      });
      cargarFotos(Number(id));
    }).catch(() => alert("Error al cargar activo"));
  }, [id, cargarFotos]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isEdit) {
        const payload: ActivoUpdate = {};
        for (const [k, v] of Object.entries(form)) {
          if (v !== undefined && v !== "") (payload as Record<string, unknown>)[k] = v;
        }
        delete (payload as Record<string, unknown>).codigo_inventario;
        await activosApi.actualizar(Number(id), payload);
        toast("Activo actualizado correctamente", "success");
        navigate("/activos");
      } else {
        const res = await activosApi.crear(form);
        toast("Activo creado correctamente. Ahora puedes agregar fotos.", "success");
        navigate(`/activos/editar/${res.data.id}`);
      }
    } catch (err) {
      console.error(`Error al ${isEdit ? "actualizar" : "crear"} activo:`, err);
      toast(`Error al ${isEdit ? "actualizar" : "crear"} el activo`, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleSubirFoto = async (file: File) => {
    if (!id) return;
    setUploadingFoto(true);
    try {
      await activosApi.subirFoto(Number(id), file);
      toast("Foto subida correctamente", "success");
      cargarFotos(Number(id));
    } catch (err) {
      console.error("Error subiendo foto:", err);
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

  const set = (field: keyof ActivoCreate) => (value: string | number | null | boolean) =>
    setForm((prev) => ({ ...prev, [field]: value }));

  return (
    <div>
      <h2>{isEdit ? "Editar Activo" : "Nuevo Activo"}</h2>
      <form onSubmit={handleSubmit}>
        <FormSection title="Información General">
          <FormField label="Código de Inventario" required>
            <input style={inputStyle} value={form.codigo_inventario} onChange={(e) => set("codigo_inventario")(e.target.value)} required />
          </FormField>
          <FormField label="Modelo" required>
            <input style={inputStyle} value={form.modelo} onChange={(e) => set("modelo")(e.target.value)} required />
          </FormField>
          <FormField label="Número de Serie" required>
            <input style={inputStyle} value={form.numero_serie} onChange={(e) => set("numero_serie")(e.target.value)} required />
          </FormField>
          <FormField label="Categoría">
            <SearchableSelect
              value={form.id_categoria ?? null}
              onChange={(v) => set("id_categoria")(v ?? null)}
              loadOptions={async () => {
                const res = await categoriasApi.listar();
                return res.data.map((c: { id: number; nombre: string }) => ({ id: c.id, label: c.nombre }));
              }}
              placeholder="Seleccionar categoría..."
            />
          </FormField>
          <FormField label="Estado" required>
            <select style={inputStyle} value={form.estado} onChange={(e) => set("estado")(e.target.value)} required>
              {ESTADOS.map((e) => (<option key={e} value={e}>{e}</option>))}
            </select>
          </FormField>
          <FormField label="Valor Depreciado">
            <input type="number" step="0.01" style={inputStyle} value={form.valor_depreciado} onChange={(e) => set("valor_depreciado")(Number(e.target.value))} />
          </FormField>
          <FormField label="Fecha de Compra">
            <input type="date" style={inputStyle} value={form.fecha_compra ?? ""} onChange={(e) => set("fecha_compra")(e.target.value || null)} />
          </FormField>
        </FormSection>

        <FormSection title="Ubicación">
          <div style={{ gridColumn: "1 / -1" }}>
            <div style={{ marginBottom: "var(--space-sm)", fontSize: "var(--font-size-sm)", color: "var(--text-muted)" }}>
              {form.latitud !== null && form.latitud !== undefined && form.longitud !== null && form.longitud !== undefined ? `${form.latitud.toFixed(4)}, ${form.longitud.toFixed(4)}` : "Haz clic en el mapa o arrastra el marcador"}
            </div>
            <MapPicker latitud={form.latitud ?? null} longitud={form.longitud ?? null} onChange={(lat, lng) => setForm((prev) => ({ ...prev, latitud: lat, longitud: lng }))} />
          </div>
        </FormSection>

        {isEdit && (
          <FormSection title="Fotos">
            <div style={{ gridColumn: "1 / -1" }}>
              <div style={fotosGrid}>
                {fotos.map((foto) => (
                  <div key={foto.id} style={fotoThumb}>
                    <img src={`http://localhost:8000/static/${foto.url}`} alt={`Foto ${foto.orden}`} style={thumbImg} />
                    <button type="button" style={deleteFotoBtn} onClick={() => handleEliminarFoto(foto)} title="Eliminar foto">
                      <Trash2 size={14} />
                    </button>
                  </div>
                ))}
              </div>
              <div style={{ marginTop: "0.5rem" }}>
                <CameraCapture onUpload={handleSubirFoto} uploading={uploadingFoto} />
              </div>
            </div>
          </FormSection>
        )}

        <div style={actionsStyle}>
          <Button type="submit" loading={loading} icon={<Save size={16} />}>Guardar</Button>
          <Button type="button" variant="secondary" icon={<ArrowLeft size={16} />} onClick={() => navigate("/activos")}>Cancelar</Button>
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
  marginTop: "var(--space-lg)",
};
