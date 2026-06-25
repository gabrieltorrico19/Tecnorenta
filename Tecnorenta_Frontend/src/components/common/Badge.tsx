interface BadgeProps {
  variant?: "default" | "success" | "danger" | "warning" | "info";
  children: string;
}

const colors: Record<string, { bg: string; color: string }> = {
  default: { bg: "#2a2a2a", color: "#a0a0a0" },
  success: { bg: "#052e16", color: "#22c55e" },
  danger: { bg: "#450a0a", color: "#ef4444" },
  warning: { bg: "#451a03", color: "#f59e0b" },
  info: { bg: "#0c1929", color: "#3b82f6" },
};

export default function Badge({ variant = "default", children }: BadgeProps) {
  const c = colors[variant];
  return (
    <span
      style={{
        display: "inline-block",
        padding: "0.15rem 0.6rem",
        borderRadius: "999px",
        fontSize: "0.75rem",
        fontWeight: 600,
        background: c.bg,
        color: c.color,
      }}
    >
      {children}
    </span>
  );
}
