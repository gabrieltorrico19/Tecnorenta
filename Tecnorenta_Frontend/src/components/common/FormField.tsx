interface FormFieldProps {
  label: string;
  children: React.ReactNode;
  required?: boolean;
}

export default function FormField({ label, children, required }: FormFieldProps) {
  return (
    <div style={styles.field}>
      <label style={styles.label}>
        {label}
        {required && <span style={styles.asterisk}> *</span>}
      </label>
      {children}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "0.35rem",
  },
  label: {
    fontSize: "0.8rem",
    fontWeight: 600,
    color: "var(--text-secondary)",
    textTransform: "uppercase",
    letterSpacing: "0.04em",
  },
  asterisk: {
    color: "var(--danger)",
  },
};
