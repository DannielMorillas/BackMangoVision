import { useState, type FormEvent } from "react";
import { AlertCircle, ArrowLeft, Leaf, Lock, Mail } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";
import { ApiError } from "../services/api";

export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const user = await login(email, password);
      navigate(user.must_change_password ? "/cambiar-clave" : "/dashboard", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Error inesperado al iniciar sesión.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col justify-center bg-surface-alt py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <Link
        to="/"
        className="absolute top-6 left-6 flex items-center gap-2 text-text-muted hover:text-primary transition-colors z-20 font-medium"
      >
        <ArrowLeft className="w-5 h-5" />
        <span className="hidden sm:inline">Volver</span>
      </Link>

      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-100/40 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[100px] pointer-events-none" />

      <div className="relative z-10 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-primary-light flex items-center justify-center shadow-lg shadow-primary/20">
            <Leaf className="w-8 h-8 text-white" />
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-text-primary font-display">
          MangoVision
        </h2>
        <p className="mt-2 text-center text-sm text-text-muted">
          Sistema de diagnóstico fitosanitario · ARA Export S.A.C.
        </p>
      </div>

      <div className="relative z-10 mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <form
          onSubmit={handleSubmit}
          aria-label="Formulario de inicio de sesión"
          className="bg-white py-8 px-4 shadow-lg shadow-black/5 sm:rounded-2xl sm:px-10 border border-border space-y-5"
        >
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-text-primary">
              Correo
            </label>
            <div className="mt-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail className="h-5 w-5 text-text-muted" aria-hidden="true" />
              </div>
              <input
                id="email"
                name="email"
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="block w-full pl-10 pr-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                placeholder="usuario@araexport.com.pe"
              />
            </div>
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-text-primary">
              Contraseña
            </label>
            <div className="mt-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-text-muted" aria-hidden="true" />
              </div>
              <input
                id="password"
                name="password"
                type="password"
                required
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full pl-10 pr-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all sm:text-sm"
                placeholder="••••••••"
              />
            </div>
          </div>

          {error && (
            <div
              role="alert"
              className="rounded-xl bg-red-50 border border-red-200 p-3 flex gap-2 text-sm text-red-700"
            >
              <AlertCircle className="h-5 w-5 shrink-0" aria-hidden="true" />
              <p>{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 px-4 rounded-xl text-sm font-semibold text-white bg-primary hover:bg-primary-light disabled:opacity-60 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all"
          >
            {submitting ? "Verificando…" : "Iniciar sesión"}
          </button>

          <div className="text-center text-sm">
            <Link
              to="/recuperar-clave"
              className="text-primary hover:text-primary-light font-medium"
            >
              ¿Olvidaste tu contraseña?
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
