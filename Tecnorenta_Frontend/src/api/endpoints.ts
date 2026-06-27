export const API_URL = import.meta.env.VITE_API_URL;

export const ENDPOINTS = {
  AUTH: {
    LOGIN: `${API_URL}/auth/login`,
    REGISTER: `${API_URL}/auth/register`,
    ME: `${API_URL}/auth/me`,
  },
  USUARIOS: `${API_URL}/usuarios`,
  ROLES: `${API_URL}/roles`,
  CLIENTES: `${API_URL}/clientes`,
  CATEGORIAS: `${API_URL}/categorias-activo`,
  ACTIVOS: `${API_URL}/activos`,
  CONTRATOS: `${API_URL}/contratos`,
  PAGOS: `${API_URL}/pagos`,
  ASIGNACIONES: `${API_URL}/asignaciones/`,
  REPORTES: `${API_URL}/reportes-incidencia`,
  MANTENIMIENTOS: `${API_URL}/mantenimientos`,
  HISTORIAL_UBICACION: `${API_URL}/historial-ubicacion`,
  CHECKLIST_ESTADO: `${API_URL}/checklist`,
  DASHBOARD: {
    STATS: `${API_URL}/dashboard/stats`,
    CONTRATOS_PROXIMOS: `${API_URL}/dashboard/contratos-proximos-vencer`,
  },
  HEALTH: `${API_URL}/health`,
};
