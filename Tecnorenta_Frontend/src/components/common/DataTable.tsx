import type { ReactNode } from "react";

interface Column<T> {
  key: string;
  label: string;
  render?: (row: T) => ReactNode;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  error?: string | null;
  onEdit?: (row: T) => void;
  onDelete?: (row: T) => void;
}

export default function DataTable<T extends { id: number }>({
  columns,
  data,
  loading,
  error,
  onEdit,
  onDelete,
}: DataTableProps<T>) {
  if (loading) return <p style={{ color: "var(--text-secondary)" }}>Cargando...</p>;
  if (error) return <p style={{ color: "var(--danger)" }}>{error}</p>;
  if (!data.length) return <p style={{ color: "var(--text-muted)" }}>Sin registros</p>;

  return (
    <div style={{ overflowX: "auto" }}>
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.label}</th>
            ))}
            {(onEdit || onDelete) && <th style={{ width: 120 }}>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              {columns.map((col) => (
                <td key={col.key}>
                  {col.render ? col.render(row) : String((row as Record<string, unknown>)[col.key] ?? "")}
                </td>
              ))}
              {(onEdit || onDelete) && (
                <td>
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    {onEdit && (
                      <button onClick={() => onEdit(row)} style={btnEdit}>
                        Editar
                      </button>
                    )}
                    {onDelete && (
                      <button onClick={() => onDelete(row)} style={btnDelete}>
                        Eliminar
                      </button>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const btnEdit: React.CSSProperties = {
  background: "none",
  border: "1px solid var(--border)",
  color: "var(--accent)",
  padding: "0.25rem 0.6rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontSize: "0.8rem",
};

const btnDelete: React.CSSProperties = {
  background: "none",
  border: "1px solid var(--border)",
  color: "var(--danger)",
  padding: "0.25rem 0.6rem",
  borderRadius: "var(--radius-sm)",
  cursor: "pointer",
  fontSize: "0.8rem",
};
