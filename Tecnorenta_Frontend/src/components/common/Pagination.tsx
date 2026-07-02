import Button from "./Button";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface PaginationProps {
  page: number;
  pages: number;
  total: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

export default function Pagination({ page, pages, total, pageSize, onPageChange }: PaginationProps) {
  if (total === 0) return null;
  const from = (page - 1) * pageSize + 1;
  const to = Math.min(page * pageSize, total);

  return (
    <div style={containerStyle}>
      <span style={infoStyle}>
        {from}–{to} de {total}
      </span>
      <div style={{ display: "flex", gap: "var(--space-sm)", alignItems: "center" }}>
        <Button
          variant="ghost"
          icon={<ChevronLeft size={16} />}
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          Anterior
        </Button>
        <span style={infoStyle}>
          Página {page} de {pages || 1}
        </span>
        <Button
          variant="ghost"
          icon={<ChevronRight size={16} />}
          disabled={page >= pages}
          onClick={() => onPageChange(page + 1)}
        >
          Siguiente
        </Button>
      </div>
    </div>
  );
}

const containerStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginTop: "var(--space-md)",
  flexWrap: "wrap",
  gap: "var(--space-sm)",
};

const infoStyle: React.CSSProperties = {
  color: "var(--text-muted)",
  fontSize: "0.85rem",
};
