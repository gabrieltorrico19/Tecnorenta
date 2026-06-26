import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader2 } from "lucide-react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  loading?: boolean;
  icon?: ReactNode;
}

const variantStyles: Record<string, React.CSSProperties> = {
  primary: {
    background: "var(--accent)",
    color: "#fff",
    border: "none",
  },
  secondary: {
    background: "transparent",
    color: "var(--text-secondary)",
    border: "1px solid var(--border)",
  },
  danger: {
    background: "var(--danger)",
    color: "#fff",
    border: "none",
  },
  ghost: {
    background: "transparent",
    color: "var(--accent)",
    border: "1px solid var(--border)",
  },
};

export default function Button({
  variant = "primary",
  loading,
  icon,
  children,
  style,
  disabled,
  ...rest
}: ButtonProps) {
  return (
    <button
      style={{
        ...baseStyle,
        ...variantStyles[variant],
        opacity: disabled || loading ? 0.6 : 1,
        cursor: disabled || loading ? "not-allowed" : "pointer",
        ...style,
      }}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <Loader2 size={16} style={{ animation: "spin 0.6s linear infinite" }} />
      ) : icon ? (
        <span style={iconStyle}>{icon}</span>
      ) : null}
      {children}
    </button>
  );
}

const baseStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  gap: "0.5rem",
  padding: "0.6rem 1.2rem",
  borderRadius: "var(--radius-sm)",
  fontWeight: 600,
  fontSize: "0.85rem",
  transition: "background .15s, opacity .15s",
};

const iconStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
};
