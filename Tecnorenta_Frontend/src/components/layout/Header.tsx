import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header style={styles.header}>
      <h1 style={styles.title}>
        <Link to="/" style={styles.link}>Tecnorenta</Link>
      </h1>
      <nav>
        <Link to="/usuarios" style={styles.navLink}>Usuarios</Link>
      </nav>
    </header>
  );
}

const styles: Record<string, React.CSSProperties> = {
  header: {
    background: "#1a73e8",
    color: "#fff",
    padding: "1rem 2rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: { fontSize: "1.5rem" },
  link: { color: "#fff", textDecoration: "none" },
  navLink: { color: "#fff", textDecoration: "none", marginLeft: "1rem" },
};
