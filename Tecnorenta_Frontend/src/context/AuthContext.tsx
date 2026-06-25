import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import { authApi, type UserProfile } from "../api/auth.api";

interface AuthContextType {
  token: string | null;
  user: UserProfile | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem("token")
  );
  const [user, setUser] = useState<UserProfile | null>(
    () => {
      const stored = localStorage.getItem("user");
      return stored ? JSON.parse(stored) : null;
    }
  );
  const [loading] = useState(false);

  useEffect(() => {
    if (token && !user) {
      authApi.me()
        .then((res) => {
          setUser(res.data);
          localStorage.setItem("user", JSON.stringify(res.data));
        })
        .catch(() => {
          setToken(null);
          setUser(null);
          localStorage.removeItem("token");
          localStorage.removeItem("user");
        });
    }
  }, [token, user]);

  const login = async (email: string, password: string) => {
    const res = await authApi.login({ email, password });
    const newToken = res.data.access_token;
    setToken(newToken);
    localStorage.setItem("token", newToken);

    const meRes = await authApi.me();
    setUser(meRes.data);
    localStorage.setItem("user", JSON.stringify(meRes.data));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider
      value={{ token, user, login, logout, isAuthenticated: !!token, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return ctx;
}
