import { type FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { usuarioApi, type UsuarioCreate } from "../../api/usuario.api";

export default function FormularioUsuario() {
  const navigate = useNavigate();
  const [form, setForm] = useState<UsuarioCreate>({
    nombre: "",
    email: "",
    password: "",
    telefono: "",
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await usuarioApi.crear(form);
      navigate("/usuarios");
    } catch {
      alert("Error al crear usuario");
    }
  };

  return (
    <div>
      <h2>Nuevo Usuario</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <input
          placeholder="Nombre"
          value={form.nombre}
          onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          required
          style={inputStyle}
        />
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
          style={inputStyle}
        />
        <input
          placeholder="Teléfono"
          value={form.telefono}
          onChange={(e) => setForm({ ...form, telefono: e.target.value })}
          style={inputStyle}
        />
        <button type="submit" style={btnStyle}>Guardar</button>
      </form>
    </div>
  );
}

const formStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "0.8rem",
  maxWidth: "400px",
  marginTop: "1rem",
};

const inputStyle: React.CSSProperties = {
  padding: "0.6rem",
  border: "1px solid #ccc",
  borderRadius: "4px",
};

const btnStyle: React.CSSProperties = {
  background: "#1a73e8",
  color: "#fff",
  border: "none",
  padding: "0.6rem",
  borderRadius: "4px",
  cursor: "pointer",
};
