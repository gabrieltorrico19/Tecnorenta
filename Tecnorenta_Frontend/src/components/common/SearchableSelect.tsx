import { useState, useEffect, useRef } from "react";

interface Option {
  id: number;
  label: string;
}

interface SearchableSelectProps {
  value: number | null;
  onChange: (value: number) => void;
  loadOptions: () => Promise<Option[]>;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
}

export default function SearchableSelect({
  value, onChange, loadOptions, placeholder = "Buscar...", disabled, required,
}: SearchableSelectProps) {
  const [options, setOptions] = useState<Option[]>([]);
  const [filtered, setFiltered] = useState<Option[]>([]);
  const [search, setSearch] = useState("");
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [focusedIdx, setFocusedIdx] = useState(0);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLoading(true);
    loadOptions().then((opts) => {
      setOptions(opts);
      setFiltered(opts);
    }).catch(() => {}).finally(() => setLoading(false));
  }, [loadOptions]);

  useEffect(() => {
    const q = search.toLowerCase();
    setFiltered(options.filter((o) => o.label?.toLowerCase().includes(q)));
    setFocusedIdx(0);
  }, [search, options]);

  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [open]);

  const selected = options.find((o) => o.id === value);

  const handleSelect = (opt: Option) => {
    onChange(opt.id);
    setSearch("");
    setOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!open) { if (e.key === "ArrowDown") setOpen(true); return; }
    if (e.key === "ArrowDown") { e.preventDefault(); setFocusedIdx((i) => Math.min(i + 1, filtered.length - 1)); }
    if (e.key === "ArrowUp") { e.preventDefault(); setFocusedIdx((i) => Math.max(i - 1, 0)); }
    if (e.key === "Enter" && filtered[focusedIdx]) { handleSelect(filtered[focusedIdx]); }
    if (e.key === "Escape") setOpen(false);
  };

  return (
    <div ref={wrapperRef} style={{ position: "relative" }}>
      <input
        value={open ? search : (selected?.label ?? "")}
        onChange={(e) => { setSearch(e.target.value); setOpen(true); }}
        onFocus={() => { setOpen(true); setSearch(""); }}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        style={inputStyle}
      />
      {open && (
        <div style={dropdown}>
          {loading && <div style={msgStyle}>Cargando...</div>}
          {!loading && filtered.length === 0 && <div style={msgStyle}>Sin resultados</div>}
          {!loading && filtered.map((opt, idx) => (
            <div
              key={opt.id}
              style={{ ...itemStyle, background: idx === focusedIdx ? "var(--bg-tertiary)" : "transparent" }}
              onClick={() => handleSelect(opt)}
              onMouseEnter={() => setFocusedIdx(idx)}
            >
              {opt.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  background: "var(--bg-secondary)",
  color: "var(--text-primary)",
  fontSize: "var(--font-size-md)",
  width: "100%",
  boxSizing: "border-box",
};

const dropdown: React.CSSProperties = {
  position: "absolute",
  top: "100%",
  left: 0,
  right: 0,
  maxHeight: 200,
  overflowY: "auto",
  background: "var(--bg-secondary)",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  zIndex: 100,
  marginTop: 2,
};

const msgStyle: React.CSSProperties = {
  padding: "0.5rem",
  color: "var(--text-muted)",
  fontSize: "0.85rem",
  textAlign: "center",
};

const itemStyle: React.CSSProperties = {
  padding: "0.5rem 0.6rem",
  cursor: "pointer",
  fontSize: "var(--font-size-md)",
  color: "var(--text-primary)",
};
