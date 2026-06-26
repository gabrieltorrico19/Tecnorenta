import { useState, type ReactNode } from "react";
import Button from "./Button";
import { Pencil, Trash2 } from "lucide-react";

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

function SkeletonRow({ cols }: { cols: number }) {
  return (
    <tr>
      {Array.from({ length: cols + 1 }).map((_, i) => (
        <td key={i}>
          <div className="skeleton" style={{ height: 14, width: i === cols ? 80 : `${60 + Math.random() * 30}%` }} />
        </td>
      ))}
    </tr>
  );
}

export default function DataTable<T extends { id: number }>({
  columns,
  data,
  loading,
  error,
  onEdit,
  onDelete,
}: DataTableProps<T>) {
  const [deletingId, setDeletingId] = useState<number | null>(null);

  if (loading) return (
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
          {Array.from({ length: 5 }).map((_, i) => (
            <SkeletonRow key={i} cols={columns.length} />
          ))}
        </tbody>
      </table>
    </div>
  );

  if (error) return (
    <div style={{ color: "var(--danger)", padding: "var(--space-lg)", textAlign: "center", fontSize: "var(--font-size-md)" }}>
      {error}
    </div>
  );

  if (!data.length) return (
    <div style={{ color: "var(--text-muted)", padding: "var(--space-xl)", textAlign: "center", fontSize: "var(--font-size-md)" }}>
      Sin registros
    </div>
  );

  const handleDelete = async (row: T) => {
    setDeletingId(row.id);
    try {
      await onDelete?.(row);
    } finally {
      setDeletingId(null);
    }
  };

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
                      <Button variant="ghost" icon={<Pencil size={14} />} onClick={() => onEdit(row)}>
                        Editar
                      </Button>
                    )}
                    {onDelete && (
                      <Button
                        variant="ghost"
                        icon={<Trash2 size={14} />}
                        loading={deletingId === row.id}
                        onClick={() => handleDelete(row)}
                      >
                        Eliminar
                      </Button>
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
