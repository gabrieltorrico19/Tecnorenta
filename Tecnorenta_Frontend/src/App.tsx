import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ToastProvider } from "./context/ToastContext";
import Layout from "./components/layout/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ListaUsuarios from "./pages/Usuarios/Lista";
import FormularioUsuario from "./pages/Usuarios/Formulario";
import ListaRoles from "./pages/Roles/Lista";
import FormularioRol from "./pages/Roles/Formulario";
import ListaClientes from "./pages/Clientes/Lista";
import FormularioCliente from "./pages/Clientes/Formulario";
import ListaActivos from "./pages/Activos/Lista";
import FormularioActivo from "./pages/Activos/Formulario";
import ListaContratos from "./pages/Contratos/Lista";
import FormularioContrato from "./pages/Contratos/Formulario";
import ListaPagos from "./pages/Pagos/Lista";
import FormularioPago from "./pages/Pagos/Formulario";
import ListaAsignaciones from "./pages/Asignaciones/Lista";
import FormularioAsignacion from "./pages/Asignaciones/Formulario";
import ListaReportes from "./pages/Reportes/Lista";
import FormularioReporte from "./pages/Reportes/Formulario";
import ListaMantenimientos from "./pages/Mantenimientos/Lista";
import FormularioMantenimiento from "./pages/Mantenimientos/Formulario";
import ListaCategorias from "./pages/Categorias/Lista";
import FormularioCategoria from "./pages/Categorias/Formulario";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/usuarios" element={<ListaUsuarios />} />
            <Route path="/usuarios/nuevo" element={<FormularioUsuario />} />
            <Route path="/usuarios/editar/:id" element={<FormularioUsuario />} />
            <Route path="/roles" element={<ListaRoles />} />
            <Route path="/roles/nuevo" element={<FormularioRol />} />
            <Route path="/roles/editar/:id" element={<FormularioRol />} />
            <Route path="/clientes" element={<ListaClientes />} />
            <Route path="/clientes/nuevo" element={<FormularioCliente />} />
            <Route path="/clientes/editar/:id" element={<FormularioCliente />} />
            <Route path="/activos" element={<ListaActivos />} />
            <Route path="/activos/nuevo" element={<FormularioActivo />} />
            <Route path="/activos/editar/:id" element={<FormularioActivo />} />
            <Route path="/contratos" element={<ListaContratos />} />
            <Route path="/contratos/nuevo" element={<FormularioContrato />} />
            <Route path="/contratos/editar/:id" element={<FormularioContrato />} />
            <Route path="/pagos" element={<ListaPagos />} />
            <Route path="/pagos/nuevo" element={<FormularioPago />} />
            <Route path="/pagos/editar/:id" element={<FormularioPago />} />
            <Route path="/asignaciones" element={<ListaAsignaciones />} />
            <Route path="/asignaciones/nuevo" element={<FormularioAsignacion />} />
            <Route path="/asignaciones/editar/:id" element={<FormularioAsignacion />} />
            <Route path="/reportes" element={<ListaReportes />} />
            <Route path="/reportes/nuevo" element={<FormularioReporte />} />
            <Route path="/reportes/editar/:id" element={<FormularioReporte />} />
            <Route path="/mantenimientos" element={<ListaMantenimientos />} />
            <Route path="/mantenimientos/nuevo" element={<FormularioMantenimiento />} />
            <Route path="/mantenimientos/editar/:id" element={<FormularioMantenimiento />} />
            <Route path="/categorias" element={<ListaCategorias />} />
            <Route path="/categorias/nuevo" element={<FormularioCategoria />} />
            <Route path="/categorias/editar/:id" element={<FormularioCategoria />} />
          </Route>
        </Routes>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
