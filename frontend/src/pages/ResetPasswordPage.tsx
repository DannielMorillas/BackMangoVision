import { useState, type FormEvent } from "react";
import { AlertCircle, ArrowLeft, CheckCircle2, KeyRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { ApiError } from "../services/api";
import { authService } from "../services/auth";

export function ResetPasswordPage() {
  const navigate = useNavigate();
  const [token, setToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (newPassword !== confirm) {
      setError("Las contraseñas no coinciden");
      return;
    }
    if (newPassword.length < 8) {
      setError("La nueva contraseña debe tener al menos 8 caracteres");
      return;
    }
    setSubmitting(true);
    try {
      await authService.resetPassword(token, newPassword);
      setSuccess(true);
      setTimeout(() => navigate("/login", { replace: true }), 2000);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Error inesperado");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-surface-alt flex flex-col items-center justify-center py-12 px-4">
      <Link
        to="/login"
        className="absolute top-6 left-6 flex items-center gap-2 text-text-muted hover:text-primary"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Volver al login</span>
      </Link>

      <div className="w-full max-w-md bg-white rounded-2xl border border-border card-shadow p-8">
        <h1 className="font-display text-2xl font-bold text-text-primary mb-2">
          Restablecer contraseña
        </h1>

        {success ? (
          <div
            role="status"
            className="rounded-xl bg-green-50 border border-green-200 p-4 flex gap-3 text-sm text-green-800"
          >
            <CheckCircle2 className="h-5 w-5 shrink-0" />
            <p>Contraseña actualizada. Redirigiendo al login…</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-5" aria-label="Restablecer contraseña">
            <div>
              <label htmlFor="token" className="block text-sm font-medium text-text-primary">
                Token
              </label>
              <div className="mt-1 relative">
                <KeyRound className="absolute top-3 left-3 h-5 w-5 text-text-muted" />
                <input
                  id="token"
                  type="text"
                  required
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary font-mono text-sm"
                  placeholder="Pega aquí el token recibido"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="newPassword"
                className="block text-sm font-medium text-text-primary"
              >
                Nueva contraseña
              </label>
              <input
                id="newPassword"
                type="password"
                required
                minLength={8}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full mt-1 px-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            <div>
              <label htmlFor="confirm" className="block text-sm font-medium text-text-primary">
                Confirmar contraseña
              </label>
              <input
                id="confirm"
                type="password"
                required
                minLength={8}
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                className="w-full mt-1 px-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            {error && (
              <div
                role="alert"
                className="rounded-xl bg-red-50 border border-red-200 p-3 text-sm text-red-700 flex gap-2"
              >
                <AlertCircle className="h-5 w-5 shrink-0" />
                <p>{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 px-4 rounded-xl text-white bg-primary hover:bg-primary-light disabled:opacity-60 font-semibold"
            >
              {submitting ? "Actualizando…" : "Restablecer contraseña"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
