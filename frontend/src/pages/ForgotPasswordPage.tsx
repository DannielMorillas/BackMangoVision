import { useState, type FormEvent } from "react";
import { AlertCircle, ArrowLeft, CheckCircle2, Mail } from "lucide-react";
import { Link } from "react-router-dom";

import { ApiError } from "../services/api";
import { authService } from "../services/auth";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [sent, setSent] = useState<string | null>(null);
  const [debugToken, setDebugToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const resp = await authService.forgotPassword(email);
      setSent(resp.message);
      setDebugToken(resp.debug_token);
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
          Recuperar contraseña
        </h1>
        <p className="text-sm text-text-muted mb-6">
          Indícanos tu correo registrado y te enviaremos un enlace de recuperación.
        </p>

        {sent ? (
          <div className="space-y-4">
            <div
              role="status"
              className="rounded-xl bg-green-50 border border-green-200 p-4 flex gap-3 text-sm text-green-800"
            >
              <CheckCircle2 className="h-5 w-5 shrink-0" />
              <p>{sent}</p>
            </div>

            {debugToken && (
              <div className="rounded-xl bg-amber-50 border border-amber-200 p-4 text-xs text-amber-800">
                <p className="font-semibold mb-1">
                  Token de prueba (solo en desarrollo)
                </p>
                <code
                  data-testid="debug-token"
                  className="break-all block bg-white border border-amber-200 rounded p-2 mt-2"
                >
                  {debugToken}
                </code>
                <p className="mt-2">
                  Pega este token en{" "}
                  <Link to="/restablecer-clave" className="underline">
                    /restablecer-clave
                  </Link>
                  .
                </p>
              </div>
            )}
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-5" aria-label="Solicitar reset">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-text-primary">
                Correo registrado
              </label>
              <div className="mt-1 relative">
                <Mail className="absolute top-3 left-3 h-5 w-5 text-text-muted" />
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 border border-border rounded-xl bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
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
              {submitting ? "Enviando…" : "Solicitar recuperación"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
