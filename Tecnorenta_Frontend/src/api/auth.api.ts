import api from "./axios";
import { ENDPOINTS } from "./endpoints";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  id: number;
  nombre: string;
  email: string;
  telefono: string | null;
  activo: boolean;
  rol_id: number;
  rol_nombre?: string;
  created_at: string;
  updated_at: string;
}

export const authApi = {
  login: (data: LoginRequest) =>
    api.post<LoginResponse>(ENDPOINTS.AUTH.LOGIN, data),
  me: () => api.get<UserProfile>(ENDPOINTS.AUTH.ME),
};
