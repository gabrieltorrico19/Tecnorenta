import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Button from "../common/Button";
import { LogOut, User } from "lucide-react";

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
        <User size={16} />
        {user?.nombre || "Usuario"}
      </span>
      <Button variant="secondary" onClick={handleLogout} icon={<LogOut size={14} />}>
        Cerrar sesión
      </Button>
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
    padding: "0 var(--space-xl)",
    gap: "var(--space-md)",
    position: "fixed",
    top: 0,
    left: "220px",
    right: 0,
    zIndex: 100,
  },
  user: {
    display: "flex",
    alignItems: "center",
    gap: "var(--space-sm)",
    color: "var(--text-primary)",
    fontSize: "var(--font-size-md)",
    fontWeight: 600,
  },
};
