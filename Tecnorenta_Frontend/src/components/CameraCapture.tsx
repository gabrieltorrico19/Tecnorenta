import { useRef, useState, useCallback, useEffect } from "react";
import { Camera, Upload, Trash2, X, RefreshCw } from "lucide-react";
import Button from "./common/Button";

interface CameraCaptureProps {
  onUpload: (file: File) => Promise<void>;
  uploading?: boolean;
  onFileSelected?: (file: File | null) => void;
}

export default function CameraCapture({ onUpload, uploading, onFileSelected }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [capturedFile, setCapturedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startCamera = useCallback(async () => {
    setError(null);
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
      setStream(s);
      if (videoRef.current) videoRef.current.srcObject = s;
    } catch {
      setError("No se pudo acceder a la cámara");
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      setStream(null);
    }
  }, [stream]);

  useEffect(() => () => stopCamera(), [stopCamera]);

  const capture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d")?.drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
      if (!blob) return;
      const file = new File([blob], `foto_${Date.now()}.jpg`, { type: "image/jpeg" });
      setCapturedFile(file);
      setPreview(URL.createObjectURL(blob));
      onFileSelected?.(file);
      stopCamera();
    }, "image/jpeg", 0.85);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setCapturedFile(file);
    setPreview(URL.createObjectURL(file));
    onFileSelected?.(file);
  };

  const handleUpload = async () => {
    if (!capturedFile) return;
    await onUpload(capturedFile);
    setCapturedFile(null);
    setPreview(null);
    onFileSelected?.(null);
  };

  const cancel = () => {
    if (preview) URL.revokeObjectURL(preview);
    setCapturedFile(null);
    setPreview(null);
    setError(null);
    onFileSelected?.(null);
  };

  return (
    <div style={container}>
      {!stream && !preview && (
        <div style={actions}>
          <Button type="button" onClick={startCamera} icon={<Camera size={16} />}>Tomar foto</Button>
          <Button type="button" variant="secondary" icon={<Upload size={16} />} onClick={() => fileInputRef.current?.click()}>
            Subir archivo
          </Button>
          <input ref={fileInputRef} type="file" accept="image/*" hidden onChange={handleFileSelect} />
        </div>
      )}

      {stream && (
        <div style={previewBox}>
          <video ref={videoRef} autoPlay playsInline style={videoStyle} />
          <canvas ref={canvasRef} hidden />
          <div style={camActions}>
            <Button type="button" onClick={capture} icon={<Camera size={16} />}>Capturar</Button>
            <Button type="button" variant="secondary" onClick={stopCamera} icon={<X size={16} />}>Cancelar</Button>
          </div>
        </div>
      )}

      {preview && capturedFile && (
        <div style={previewBox}>
          <img src={preview} alt="Preview" style={imgPreview} />
          <div style={camActions}>
            <Button type="button" onClick={handleUpload} loading={uploading} icon={<Upload size={16} />}>Subir foto</Button>
            <Button type="button" variant="ghost" onClick={startCamera} icon={<RefreshCw size={16} />}>Repetir</Button>
            <Button type="button" variant="secondary" onClick={cancel} icon={<Trash2 size={16} />}>Descartar</Button>
          </div>
        </div>
      )}

      {error && <p style={errorStyle}>{error}</p>}
    </div>
  );
}

const container: React.CSSProperties = { display: "flex", flexDirection: "column", gap: "0.5rem" };
const actions: React.CSSProperties = { display: "flex", gap: "0.5rem", flexWrap: "wrap" };
const previewBox: React.CSSProperties = { display: "flex", flexDirection: "column", gap: "0.5rem", alignItems: "flex-start" };
const videoStyle: React.CSSProperties = { maxWidth: "100%", borderRadius: "var(--radius-sm)", border: "1px solid var(--border)", maxHeight: 300 };
const imgPreview: React.CSSProperties = { maxWidth: "100%", maxHeight: 300, borderRadius: "var(--radius-sm)", border: "1px solid var(--border)" };
const camActions: React.CSSProperties = { display: "flex", gap: "0.5rem", flexWrap: "wrap" };
const errorStyle: React.CSSProperties = { color: "var(--danger)", fontSize: "0.85rem" };
