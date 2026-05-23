import { Leaf, LogOut, Sparkles } from "lucide-react";

import { useAuth } from "../hooks/AuthContext";

export function DashboardPage() {
  const { user, logout } = useAuth();
  if (!user) return null;

  return (
    <div className="min-h-screen bg-surface">
      <nav className="bg-white border-b border-border px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-primary-light flex items-center justify-center">
            <Leaf className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-display font-bold text-lg text-text-primary">MangoVision</p>
            <p className="text-xs text-text-muted">
              {user.first_name} {user.last_name} · {user.role}
            </p>
          </div>
        </div>
        <button
          data-testid="logout-button"
          onClick={() => void logout()}
          className="flex items-center gap-2 px-3 py-2 rounded-xl text-text-muted hover:text-red-500 hover:bg-red-50 transition-colors text-sm font-medium"
        >
          <LogOut className="w-4 h-4" />
          Cerrar sesión
        </button>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-12">
        <div className="bg-white border border-border rounded-2xl p-8 card-shadow flex gap-6 items-start">
          <div className="w-12 h-12 rounded-xl bg-primary-50 border border-primary-100 flex items-center justify-center shrink-0">
            <Sparkles className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="font-display text-2xl font-bold text-text-primary mb-2">
              Bienvenido, {user.first_name}
            </h1>
            <p className="text-text-muted">
              El dashboard real (HU-011) se construye en el Sprint 4. Por ahora ya estás
              autenticado dentro del sistema — login + JWT + ruta protegida funcionando.
            </p>
            {user.role === "admin" && (
              <a
                href="/admin/usuarios"
                className="inline-block mt-4 text-sm font-medium text-primary hover:text-primary-light"
              >
                Ir a gestión de usuarios →
              </a>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
