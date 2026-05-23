import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Navigate, Route, Routes } from "react-router-dom";

import { LoginPage } from "../LoginPage";
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

function StubDashboard() {
  return <div data-testid="dashboard-stub">DASHBOARD</div>;
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<StubDashboard />} />
      <Route path="/cambiar-clave" element={<div data-testid="change-pwd-stub" />} />
      <Route path="/" element={<Navigate to="/login" replace />} />
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

describe("LoginPage (HU-004, HU-005, HU-006 link)", () => {
  it("HU-004 · envía credenciales y redirige al dashboard tras login OK", async () => {
    global.fetch = vi.fn(async (url: RequestInfo | URL) => {
      if (String(url).endsWith("/auth/login")) {
        return new Response(
          JSON.stringify({
            access_token: "fake.jwt.token",
            token_type: "bearer",
            expires_in_seconds: 28800,
            user: mockUser,
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        );
      }
      return new Response("not stubbed", { status: 500 });
    }) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/login" });
    await userEvent.type(screen.getByLabelText(/Correo/i), "ada@example.com");
    await userEvent.type(screen.getByLabelText(/Contraseña/i), "ClaveSegura123");
    await userEvent.click(screen.getByRole("button", { name: /Iniciar sesión/i }));

    await waitFor(() => {
      expect(screen.getByTestId("dashboard-stub")).toBeInTheDocument();
    });
    expect(localStorage.getItem("mangovision_token")).toBe("fake.jwt.token");
  });

  it("HU-004 · muestra mensaje de error si las credenciales son inválidas", async () => {
    global.fetch = vi.fn(async () =>
      new Response(JSON.stringify({ detail: "Credenciales inválidas" }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      }),
    ) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/login" });
    await userEvent.type(screen.getByLabelText(/Correo/i), "ada@example.com");
    await userEvent.type(screen.getByLabelText(/Contraseña/i), "incorrecta");
    await userEvent.click(screen.getByRole("button", { name: /Iniciar sesión/i }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/Credenciales inválidas/i);
    });
    expect(localStorage.getItem("mangovision_token")).toBeNull();
  });

  it("HU-004 · si must_change_password=true, redirige a /cambiar-clave", async () => {
    global.fetch = vi.fn(async () =>
      new Response(
        JSON.stringify({
          access_token: "fake.jwt.token",
          token_type: "bearer",
          expires_in_seconds: 28800,
          user: { ...mockUser, must_change_password: true },
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    ) as unknown as typeof fetch;

    renderWithProviders(<App />, { initialPath: "/login" });
    await userEvent.type(screen.getByLabelText(/Correo/i), "ada@example.com");
    await userEvent.type(screen.getByLabelText(/Contraseña/i), "ClaveTemporal123");
    await userEvent.click(screen.getByRole("button", { name: /Iniciar sesión/i }));

    await waitFor(() => {
      expect(screen.getByTestId("change-pwd-stub")).toBeInTheDocument();
    });
  });

  it("HU-006 · enlace 'Olvidaste tu contraseña' lleva a /recuperar-clave", () => {
    renderWithProviders(<App />, { initialPath: "/login" });
    const link = screen.getByRole("link", { name: /Olvidaste tu contraseña/i });
    expect(link).toHaveAttribute("href", "/recuperar-clave");
  });
});
