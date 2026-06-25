import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function Layout() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return null;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div style={styles.layout}>
      <Sidebar />
      <Header />
      <main style={styles.main}>
        <Outlet />
      </main>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  layout: {
    display: "flex",
    minHeight: "100vh",
  },
  main: {
    marginLeft: "220px",
    marginTop: "56px",
    flex: 1,
    padding: "2rem",
    background: "var(--bg-primary)",
    minHeight: "calc(100vh - 56px)",
  },
};
