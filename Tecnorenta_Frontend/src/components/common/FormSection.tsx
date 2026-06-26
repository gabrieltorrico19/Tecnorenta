import type { ReactNode } from "react";

interface FormSectionProps {
  title: string;
  children: ReactNode;
}

export default function FormSection({ title, children }: FormSectionProps) {
  return (
    <div style={section}>
      <h3 style={heading}>{title}</h3>
      <div style={grid}>{children}</div>
    </div>
  );
}

const section: React.CSSProperties = {
  marginBottom: "var(--space-lg)",
};

const heading: React.CSSProperties = {
  fontSize: "var(--font-size-md)",
  fontWeight: 700,
  color: "var(--text-primary)",
  margin: "0 0 var(--space-sm) 0",
  paddingBottom: "var(--space-xs)",
  borderBottom: "1px solid var(--border)",
};

const grid: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
  gap: "var(--space-md)",
};
