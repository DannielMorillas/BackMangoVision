import { useEffect, useState, type FormEvent } from "react";
import { ArrowLeft, Check, CircleSlash, Plus, UserPlus, X } from "lucide-react";
import { Link } from "react-router-dom";

import { ApiError } from "../services/api";
import { adminService, type CreateUserPayload } from "../services/admin";
import type { User, UserRole } from "../types/user";

const ROLES: { value: UserRole; label: string }[] = [
  { value: "admin", label: "Administrador" },
  { value: "agronomist", label: "Ingeniero agrónomo" },
  { value: "technician", label: "Técnico" },
];

export function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const [form, setForm] = useState<CreateUserPayload>({
    email: "",
    first_name: "",
    last_name: "",
    role: "agronomist",
    temp_password: "",
  });

  async function reload() {
    setLoading(true);
    try {
      setUsers(await adminService.listUsers());
      setError(null);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Error al cargar usuarios");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void reload();
  }, []);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);
    try {
      await adminService.createUser(form);
      setForm({ email: "", first_name: "", last_name: "", role: "agronomist", temp_password: "" });
      setShowForm(false);
      await reload();
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : "Error al crear usuario");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggle(user: User) {
    try {
      await adminService.setStatus(user.id, !user.is_active);
      await reload();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Error al cambiar estado");
    }
  }

  return (
    <div className="min-h-screen bg-surface">
      <header className="bg-white border-b border-border px-6 py-4 flex items-center justify-between">
        <Link
          to="/dashboard"
          className="flex items-center gap-2 text-text-muted hover:text-primary"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Dashboard</span>
        </Link>
        <h1 className="font-display text-lg font-bold text-text-primary">
          Gestión de usuarios
        </h1>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-white hover:bg-primary-light text-sm font-medium"
        >
          {showForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showForm ? "Cancelar" : "Nuevo usuario"}
        </button>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        {showForm && (
          <form
            onSubmit={handleCreate}
            aria-label="Crear usuario"
            className="bg-white border border-border rounded-2xl p-6 card-shadow grid md:grid-cols-2 gap-4"
          >
            <div>
              <label className="block text-sm font-medium text-text-primary">Nombre</label>
              <input
                required
                value={form.first_name}
                onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                className="w-full mt-1 px-3 py-2 border border-border rounded-lg bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary">Apellido</label>
              <input
                required
                value={form.last_name}
                onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                className="w-full mt-1 px-3 py-2 border border-border rounded-lg bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary">Correo</label>
              <input
                required
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full mt-1 px-3 py-2 border border-border rounded-lg bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-primary">Rol</label>
              <select
                value={form.role}
                onChange={(e) => setForm({ ...form, role: e.target.value as UserRole })}
                className="w-full mt-1 px-3 py-2 border border-border rounded-lg bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary"
              >
                {ROLES.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-text-primary">
                Contraseña temporal (≥ 8 caracteres)
              </label>
              <input
                required
                minLength={8}
                value={form.temp_password}
                onChange={(e) => setForm({ ...form, temp_password: e.target.value })}
                className="w-full mt-1 px-3 py-2 border border-border rounded-lg bg-surface-alt focus:outline-none focus:ring-2 focus:ring-primary font-mono text-sm"
              />
              <p className="text-xs text-text-muted mt-1">
                El usuario deberá cambiarla en su primer inicio de sesión.
              </p>
            </div>

            {formError && (
              <div
                role="alert"
                className="md:col-span-2 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700"
              >
                {formError}
              </div>
            )}

            <div className="md:col-span-2 flex justify-end gap-2">
              <button
                type="submit"
                disabled={submitting}
                className="px-5 py-2.5 rounded-xl bg-primary text-white hover:bg-primary-light disabled:opacity-60 text-sm font-semibold flex items-center gap-2"
              >
                <UserPlus className="w-4 h-4" />
                {submitting ? "Creando…" : "Crear usuario"}
              </button>
            </div>
          </form>
        )}

        {error && (
          <div
            role="alert"
            className="rounded-xl bg-red-50 border border-red-200 p-4 text-sm text-red-700"
          >
            {error}
          </div>
        )}

        <section className="bg-white border border-border rounded-2xl card-shadow overflow-hidden">
          {loading ? (
            <p className="p-6 text-text-muted text-sm">Cargando…</p>
          ) : (
            <table className="w-full text-sm" aria-label="Listado de usuarios">
              <thead className="bg-surface-alt text-left text-text-muted text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-3">Usuario</th>
                  <th className="px-6 py-3">Correo</th>
                  <th className="px-6 py-3">Rol</th>
                  <th className="px-6 py-3">Estado</th>
                  <th className="px-6 py-3 text-right">Acción</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr
                    key={u.id}
                    data-testid={`user-row-${u.id}`}
                    className="border-t border-border"
                  >
                    <td className="px-6 py-3">
                      {u.first_name} {u.last_name}
                    </td>
                    <td className="px-6 py-3 text-text-muted">{u.email}</td>
                    <td className="px-6 py-3">{u.role}</td>
                    <td className="px-6 py-3">
                      {u.is_active ? (
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                          <Check className="w-3 h-3" /> Activo
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium bg-red-50 text-red-700 border border-red-200">
                          <CircleSlash className="w-3 h-3" /> Inactivo
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-3 text-right">
                      <button
                        onClick={() => void handleToggle(u)}
                        data-testid={`toggle-status-${u.id}`}
                        className="text-sm text-primary hover:text-primary-light font-medium"
                      >
                        {u.is_active ? "Desactivar" : "Activar"}
                      </button>
                    </td>
                  </tr>
                ))}
                {users.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-text-muted">
                      No hay usuarios registrados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}
