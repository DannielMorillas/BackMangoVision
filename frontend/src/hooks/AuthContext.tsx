import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { getStoredToken, setStoredToken } from "../services/api";
import { authService } from "../services/auth";
import type { User } from "../types/user";

interface AuthContextValue {
  user: User | null;
  status: "loading" | "anonymous" | "authenticated";
  login: (email: string, password: string) => Promise<User>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [status, setStatus] = useState<AuthContextValue["status"]>(
    getStoredToken() ? "loading" : "anonymous",
  );

  useEffect(() => {
    if (!getStoredToken()) {
      setStatus("anonymous");
      return;
    }
    let cancelled = false;
    authService
      .me()
      .then((u) => {
        if (cancelled) return;
        setUser(u);
        setStatus("authenticated");
      })
      .catch(() => {
        if (cancelled) return;
        setStoredToken(null);
        setUser(null);
        setStatus("anonymous");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const resp = await authService.login({ email, password });
    setStoredToken(resp.access_token);
    setUser(resp.user);
    setStatus("authenticated");
    return resp.user;
  }, []);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch {
      /* incluso si el server falla, seguimos limpiando el cliente */
    }
    setStoredToken(null);
    setUser(null);
    setStatus("anonymous");
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({ user, status, login, logout }),
    [user, status, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <AuthProvider>");
  return ctx;
}
