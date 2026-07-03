import type { ReactNode } from "react";
import Button from "./Button";
import { FilterX } from "lucide-react";

interface FilterBarProps {
  children: ReactNode;
  /** Se muestra el botón "Limpiar" solo si hay filtros activos. */
  hayFiltros?: boolean;
  onLimpiar?: () => void;
}

/** Fila de controles de filtro para las listas (filtrado del lado del servidor). */
export default function FilterBar({ children, hayFiltros, onLimpiar }: FilterBarProps) {
  return (
    <div style={rowStyle}>
      {children}
      {onLimpiar && hayFiltros && (
        <Button variant="ghost" icon={<FilterX size={14} />} onClick={onLimpiar}>
          Limpiar
        </Button>
      )}
    </div>
  );
}

const rowStyle: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: "var(--space-sm)",
  alignItems: "center",
  marginBottom: "var(--space-md)",
};
