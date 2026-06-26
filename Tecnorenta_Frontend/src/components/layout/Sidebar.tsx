import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard", icon: "▦" },
  { to: "/usuarios", label: "Usuarios", icon: "👤" },
  { to: "/roles", label: "Roles", icon: "🔐" },
  { to: "/clientes", label: "Clientes", icon: "👥" },
  { to: "/activos", label: "Activos", icon: "💻" },
  { to: "/categorias", label: "Categorías", icon: "📂" },
  { to: "/contratos", label: "Contratos", icon: "📄" },
  { to: "/pagos", label: "Pagos", icon: "💰" },
  { to: "/asignaciones", label: "Asignaciones", icon: "📋" },
  { to: "/reportes", label: "Reportes", icon: "⚠️" },
  { to: "/mantenimientos", label: "Mantenimiento", icon: "🔧" },
];

export default function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      <div style={styles.logo}>T</div>
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
    fontSize: "1.5rem",
    fontWeight: 800,
    color: "var(--accent)",
    padding: "1.25rem",
    textAlign: "center",
    borderBottom: "1px solid var(--border)",
  },
  nav: {
    display: "flex",
    flexDirection: "column",
    padding: "0.5rem 0",
  },
  link: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    padding: "0.65rem 1.25rem",
    color: "var(--text-secondary)",
    textDecoration: "none",
    fontSize: "0.9rem",
    transition: "background .15s",
  },
  icon: {
    fontSize: "1rem",
    width: "1.25rem",
    textAlign: "center",
  },
};
