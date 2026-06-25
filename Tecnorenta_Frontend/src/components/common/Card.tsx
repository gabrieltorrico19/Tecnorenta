import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  children: ReactNode;
  style?: React.CSSProperties;
}

export default function Card({ title, children, style }: CardProps) {
  return (
    <div style={{ ...styles.card, ...style }}>
      {title && <h3 style={styles.title}>{title}</h3>}
      {children}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    padding: "1.5rem",
  },
  title: {
    fontSize: "1rem",
    fontWeight: 600,
    color: "var(--text-primary)",
    marginBottom: "1rem",
  },
};
