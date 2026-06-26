import { useEffect, type ReactNode } from "react";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export default function Modal({ open, onClose, title, children }: ModalProps) {
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.header}>
          <h3 style={styles.title}>{title}</h3>
          <button onClick={onClose} style={styles.close}>✕</button>
        </div>
        <div style={styles.body}>{children}</div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,.6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
    padding: "var(--space-md)",
    animation: "fadeIn .15s ease-out",
  },
  modal: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    width: "100%",
    maxWidth: "500px",
    maxHeight: "80vh",
    overflowY: "auto",
    animation: "fadeIn .15s ease-out",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "var(--space-md) var(--space-lg)",
    borderBottom: "1px solid var(--border)",
  },
  title: {
    fontSize: "var(--font-size-lg)",
    fontWeight: 700,
    color: "var(--text-primary)",
  },
  close: {
    background: "none",
    border: "none",
    color: "var(--text-muted)",
    fontSize: "1.2rem",
    cursor: "pointer",
    padding: "var(--space-xs)",
    borderRadius: "var(--radius-sm)",
    transition: "color .15s",
  },
  body: {
    padding: "var(--space-lg)",
  },
};
