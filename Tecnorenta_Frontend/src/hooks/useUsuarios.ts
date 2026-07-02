import { useState, useEffect, useCallback } from "react";
import { usuarioApi } from "../api/usuario.api";
import type { Usuario, UsuarioCreate, UsuarioUpdate } from "../api/usuario.api";

export function useUsuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listar = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await usuarioApi.listarTodos();
      setUsuarios(data);
    } catch {
      setError("Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  }, []);

  const crear = useCallback(async (data: UsuarioCreate) => {
    const res = await usuarioApi.crear(data);
    setUsuarios((prev) => [...prev, res.data]);
    return res.data;
  }, []);

  const actualizar = useCallback(async (id: number, data: UsuarioUpdate) => {
    const res = await usuarioApi.actualizar(id, data);
    setUsuarios((prev) => prev.map((u) => (u.id === id ? res.data : u)));
    return res.data;
  }, []);

  const eliminar = useCallback(async (id: number) => {
    await usuarioApi.eliminar(id);
    setUsuarios((prev) => prev.filter((u) => u.id !== id));
  }, []);

  useEffect(() => {
    listar();
  }, [listar]);

  return { usuarios, loading, error, listar, crear, actualizar, eliminar };
}
