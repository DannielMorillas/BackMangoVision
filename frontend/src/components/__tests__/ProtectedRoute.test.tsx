import { screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "../ProtectedRoute";
import { renderWithProviders } from "../../test/render";

const mockUser = {
  id: 1,
  email: "ada@example.com",
  first_name: "Ada",
  last_name: "Perez",
  role: "agronomist" as const,
  is_active: true,
  must_change_password: false,
  created_at: "2026-05-23T00:00:00Z",
  last_login_at: null,
};

const originalFetch = global.fetch;

function App() {
  return (
    <Routes>
      <Route path="/login" element={<div data-testid="login-page">LOGIN</div>} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <div data-testid="dashboard-page">DASHBOARD</div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute requireRole="admin">
            <div data-testid="admin-page">ADMIN</div>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

beforeEach(() => {
  localStorage.clear();
});

afterEach(() => {
  global.fetch = originalFetch;
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("ProtectedRoute (HU-005, HU-007)", () => {
  it("redirige a /login si no hay token guardado", async () => {
    renderWithProviders(<App />, { initialPath: "/dashboard" });
    await waitFor(() => {
      expect(screen.getByTestId("login-page")).toBeInTheDocument();
    });
  });

  it("renderiza el contenido si el token es válido y /me devuelve usuario", async () => {
    localStorage.setItem("mangovision_token", "fake.jwt");
    global.fetch = vi.fn(async (url: RequestInfo | URL) => {
      if (String(url).endsWith("/auth/me")) {
        return new Response(JSON.stringify(mockUser), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        });
      }
      return new Response("nope", { status: 500 });
    }) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/dashboard" });
    await waitFor(() => {
      expect(screen.getByTestId("dashboard-page")).toBeInTheDocument();
    });
  });

  it("redirige a /login si /me devuelve 401 (token inválido)", async () => {
    localStorage.setItem("mangovision_token", "fake.jwt");
    global.fetch = vi.fn(async () =>
      new Response(JSON.stringify({ detail: "No autenticado" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      }),
    ) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/dashboard" });
    await waitFor(() => {
      expect(screen.getByTestId("login-page")).toBeInTheDocument();
    });
    expect(localStorage.getItem("mangovision_token")).toBeNull();
  });

  it("bloquea acceso a /admin si el usuario no es admin (rol agronomist)", async () => {
    localStorage.setItem("mangovision_token", "fake.jwt");
    global.fetch = vi.fn(async () =>
      new Response(JSON.stringify(mockUser), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    ) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/admin" });
    await waitFor(() => {
      expect(screen.queryByTestId("admin-page")).not.toBeInTheDocument();
    });
  });

  it("permite acceso a /admin si rol = admin", async () => {
    localStorage.setItem("mangovision_token", "fake.jwt");
    global.fetch = vi.fn(async () =>
      new Response(JSON.stringify({ ...mockUser, role: "admin" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    ) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/admin" });
    await waitFor(() => {
      expect(screen.getByTestId("admin-page")).toBeInTheDocument();
    });
  });
});
