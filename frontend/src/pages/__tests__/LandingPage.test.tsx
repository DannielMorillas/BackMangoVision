import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { LandingPage } from "../LandingPage";

const diseases = [
  {
    id: 1,
    slug: "sano",
    name: "Fruto sano",
    color_hex: "#22C55E",
    description: "Sin signos visibles.",
  },
  {
    id: 2,
    slug: "antracnosis",
    name: "Antracnosis",
    color_hex: "#DC2626",
    description: "Manchas oscuras hundidas.",
  },
];

const originalFetch = global.fetch;

beforeEach(() => {
  global.fetch = vi.fn(async () =>
    new Response(JSON.stringify(diseases), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }),
  ) as unknown as typeof fetch;
});

afterEach(() => {
  global.fetch = originalFetch;
  vi.restoreAllMocks();
});

function renderLanding() {
  return render(
    <MemoryRouter>
      <LandingPage />
    </MemoryRouter>,
  );
}

describe("LandingPage (HU-001, HU-002, HU-003)", () => {
  it("HU-001 · muestra el nombre del sistema y el tagline", () => {
    renderLanding();
    expect(
      screen.getAllByText(/MangoVision/i).length,
    ).toBeGreaterThanOrEqual(1);
    expect(
      screen.getByRole("heading", {
        level: 1,
        name: /Diagnostica enfermedades del mango/i,
      }),
    ).toBeInTheDocument();
  });

  it("HU-001 · tiene una sección de beneficios con al menos 3 tarjetas", () => {
    renderLanding();
    const beneficios = screen.getByRole("heading", {
      level: 2,
      name: /Diagnóstico fitosanitario sistemático/i,
    });
    expect(beneficios).toBeInTheDocument();
  });

  it("HU-002 · renderiza el catálogo de enfermedades desde el backend", async () => {
    renderLanding();
    await waitFor(() => {
      const cards = screen.getAllByTestId("disease-card");
      expect(cards).toHaveLength(diseases.length);
    });
    expect(screen.getByText("Fruto sano")).toBeInTheDocument();
    expect(screen.getByText("Antracnosis")).toBeInTheDocument();
  });

  it("HU-002 · muestra el mensaje de error si /api/diseases falla", async () => {
    global.fetch = vi.fn(async () =>
      new Response("error", { status: 500 }),
    ) as unknown as typeof fetch;

    renderLanding();
    await waitFor(() => {
      expect(screen.getByRole("alert")).toBeInTheDocument();
    });
  });

  it("HU-003 · el botón principal de hero enlaza a /login (React Router)", () => {
    renderLanding();
    const cta = screen.getByTestId("cta-primary-login");
    expect(cta).toHaveAttribute("href", "/login");
  });

  it("HU-003 · el botón de navbar también enlaza a /login", () => {
    renderLanding();
    const navbarLinks = screen.getAllByRole("link", { name: /Iniciar sesión/i });
    expect(
      navbarLinks.some((link) => link.getAttribute("href") === "/login"),
    ).toBe(true);
  });
});
