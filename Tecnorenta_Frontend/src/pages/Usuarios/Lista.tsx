import { useUsuarios } from "../../hooks/useUsuarios";

export default function ListaUsuarios() {
  const { usuarios, loading, error, eliminar } = useUsuarios();

  if (loading) return <p>Cargando usuarios...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h2>Usuarios</h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Activo</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.nombre}</td>
              <td>{u.email}</td>
              <td>{u.telefono || "—"}</td>
              <td>{u.activo ? "✅" : "❌"}</td>
              <td>
                <button onClick={() => eliminar(u.id)} style={btnStyle}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const tableStyle: React.CSSProperties = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "1rem",
};

const btnStyle: React.CSSProperties = {
  background: "#e74c3c",
  color: "#fff",
  border: "none",
  padding: "0.3rem 0.8rem",
  borderRadius: "4px",
  cursor: "pointer",
};
