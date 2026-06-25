import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header style={styles.header}>
      <span style={styles.user}>
        {user?.nombre || "Usuario"}
      </span>
      <button onClick={handleLogout} style={styles.logout}>
        Cerrar sesión
      </button>
    </header>
  );
}

const styles: Record<string, React.CSSProperties> = {
  header: {
    height: "56px",
    background: "var(--bg-secondary)",
    borderBottom: "1px solid var(--border)",
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: "0 2rem",
    gap: "1rem",
    position: "fixed",
    top: 0,
    left: "220px",
    right: 0,
    zIndex: 100,
  },
  user: {
    color: "var(--text-primary)",
    fontSize: "0.9rem",
    fontWeight: 600,
  },
  logout: {
    background: "none",
    border: "1px solid var(--border)",
    color: "var(--text-secondary)",
    padding: "0.35rem 0.75rem",
    borderRadius: "var(--radius-sm)",
    cursor: "pointer",
    fontSize: "0.8rem",
  },
};
