import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from "lucide-react";

type ToastType = "success" | "error" | "warning" | "info";

interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

interface ToastContextType {
  toast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

const iconMap = {
  success: <CheckCircle size={18} />,
  error: <AlertCircle size={18} />,
  warning: <AlertTriangle size={18} />,
  info: <Info size={18} />,
};

const colorMap: Record<ToastType, string> = {
  success: "var(--success)",
  error: "var(--danger)",
  warning: "var(--warning)",
  info: "var(--accent)",
};

let nextId = 0;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: ToastType = "info") => {
    const id = nextId++;
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toast: addToast }}>
      {children}
      <div style={containerStyle}>
        {toasts.map((t) => (
          <div key={t.id} style={{ ...toastStyle, borderLeft: `3px solid ${colorMap[t.type]}` }}>
            <span style={{ color: colorMap[t.type], display: "flex" }}>{iconMap[t.type]}</span>
            <span style={{ flex: 1 }}>{t.message}</span>
            <button onClick={() => removeToast(t.id)} style={closeBtnStyle}>
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}

const containerStyle: React.CSSProperties = {
  position: "fixed",
  top: "1rem",
  right: "1rem",
  zIndex: 9999,
  display: "flex",
  flexDirection: "column",
  gap: "0.5rem",
  maxWidth: "360px",
};

const toastStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: "0.6rem",
  background: "var(--bg-secondary)",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  padding: "0.75rem 1rem",
  color: "var(--text-primary)",
  fontSize: "0.85rem",
  boxShadow: "0 4px 12px rgba(0,0,0,.4)",
  animation: "slideIn .2s ease-out",
};

const closeBtnStyle: React.CSSProperties = {
  background: "none",
  border: "none",
  color: "var(--text-muted)",
  cursor: "pointer",
  padding: 0,
  display: "flex",
};
