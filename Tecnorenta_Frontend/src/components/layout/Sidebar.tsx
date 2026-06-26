import { NavLink } from "react-router-dom";
import { LayoutDashboard, Users, Shield, Building2, Monitor, FileText, DollarSign, ClipboardList, AlertTriangle, Wrench, FolderTree, MapPin, ClipboardCheck } from "lucide-react";
import type { ReactNode } from "react";

interface LinkItem {
  to: string;
  label: string;
  icon: ReactNode;
}

const links: LinkItem[] = [
  { to: "/", label: "Dashboard", icon: <LayoutDashboard size={18} /> },
  { to: "/usuarios", label: "Usuarios", icon: <Users size={18} /> },
  { to: "/roles", label: "Roles", icon: <Shield size={18} /> },
  { to: "/clientes", label: "Clientes", icon: <Building2 size={18} /> },
  { to: "/activos", label: "Activos", icon: <Monitor size={18} /> },
  { to: "/categorias", label: "Categorías", icon: <FolderTree size={18} /> },
  { to: "/contratos", label: "Contratos", icon: <FileText size={18} /> },
  { to: "/pagos", label: "Pagos", icon: <DollarSign size={18} /> },
  { to: "/asignaciones", label: "Asignaciones", icon: <ClipboardList size={18} /> },
  { to: "/reportes", label: "Reportes", icon: <AlertTriangle size={18} /> },
  { to: "/mantenimientos", label: "Mantenimiento", icon: <Wrench size={18} /> },
  { to: "/historial-ubicacion", label: "Historial Ubicación", icon: <MapPin size={18} /> },
  { to: "/checklist", label: "Checklist Estado", icon: <ClipboardCheck size={18} /> },
];

export default function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      <div style={styles.logo}>SIGTAR</div>
      <nav style={styles.nav}>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            style={({ isActive }) => ({
              ...styles.link,
              background: isActive ? "var(--bg-tertiary)" : "transparent",
              borderRight: isActive ? "2px solid var(--accent)" : "2px solid transparent",
            })}
          >
            <span style={styles.icon}>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

const styles: Record<string, React.CSSProperties> = {
  sidebar: {
    width: "220px",
    minHeight: "100vh",
    background: "var(--bg-secondary)",
    borderRight: "1px solid var(--border)",
    display: "flex",
    flexDirection: "column",
    position: "fixed",
    left: 0,
    top: 0,
  },
  logo: {
    fontSize: "var(--font-size-xl)",
    fontWeight: 800,
    color: "var(--accent)",
    padding: "var(--space-lg)",
    textAlign: "center",
    borderBottom: "1px solid var(--border)",
    letterSpacing: "0.05em",
  },
  nav: {
    display: "flex",
    flexDirection: "column",
    padding: "var(--space-sm) 0",
  },
  link: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-md)",
    padding: "var(--space-sm) var(--space-lg)",
    color: "var(--text-secondary)",
    textDecoration: "none",
    fontSize: "var(--font-size-md)",
    transition: "background .15s, color .15s",
  },
  icon: {
    display: "inline-flex",
    alignItems: "center",
    width: "20px",
    justifyContent: "center",
  },
};
