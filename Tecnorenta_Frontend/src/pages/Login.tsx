import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Button from "../components/common/Button";
import { LogIn } from "lucide-react";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch {
      setError("Credenciales inválidas");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.wrapper}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <div style={styles.logoArea}>
          <div style={styles.logoIcon}>ST</div>
          <h1 style={styles.title}>SIGTAR</h1>
        </div>
        <p style={styles.subtitle}>Sistema de Gestión y Trazabilidad de Activos Rentados</p>
        {error && <p style={styles.error}>{error}</p>}
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={styles.input}
        />
        <Button type="submit" loading={loading} icon={<LogIn size={16} />} style={{ width: "100%", justifyContent: "center", padding: "0.75rem" }}>
          Ingresar
        </Button>
      </form>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "var(--bg-primary)",
    padding: "var(--space-md)",
  },
  card: {
    background: "var(--bg-secondary)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    padding: "var(--space-2xl)",
    width: "100%",
    maxWidth: "400px",
    display: "flex",
    flexDirection: "column",
    gap: "var(--space-md)",
  },
  logoArea: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "var(--space-sm)",
    marginBottom: "var(--space-sm)",
  },
  logoIcon: {
    width: 48,
    height: 48,
    borderRadius: "var(--radius)",
    background: "var(--accent)",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 800,
    fontSize: "1.2rem",
  },
  title: {
    fontSize: "var(--font-size-2xl)",
    fontWeight: 700,
    color: "var(--text-primary)",
    textAlign: "center",
    letterSpacing: "0.05em",
  },
  subtitle: {
    color: "var(--text-secondary)",
    textAlign: "center",
    fontSize: "var(--font-size-sm)",
    marginBottom: "var(--space-sm)",
  },
  error: {
    color: "var(--danger)",
    fontSize: "var(--font-size-md)",
    textAlign: "center",
  },
  input: {
    padding: "0.75rem",
    borderRadius: "var(--radius-sm)",
    border: "1px solid var(--border)",
    background: "var(--bg-tertiary)",
    color: "var(--text-primary)",
    outline: "none",
  },
};
