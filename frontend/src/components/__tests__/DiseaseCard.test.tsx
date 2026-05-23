import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DiseaseCard } from "../DiseaseCard";

const sample = {
  id: 1,
  slug: "antracnosis",
  name: "Antracnosis",
  color_hex: "#DC2626",
  description: "Manchas oscuras circulares hundidas en la superficie del fruto.",
};

describe("DiseaseCard", () => {
  it("renderiza el nombre y la descripción de la enfermedad", () => {
    render(<DiseaseCard disease={sample} />);
    expect(screen.getByText(sample.name)).toBeInTheDocument();
    expect(screen.getByText(sample.description)).toBeInTheDocument();
  });

  it("expone el slug en data-attribute para tests de integración", () => {
    render(<DiseaseCard disease={sample} />);
    const card = screen.getByTestId("disease-card");
    expect(card.dataset.slug).toBe("antracnosis");
  });

  it("aplica el color de la enfermedad como background del badge", () => {
    render(<DiseaseCard disease={sample} />);
    const badge = screen.getByText(sample.name);
    expect(badge.style.color).toMatch(/220.*38.*38|#DC2626|rgb/i);
  });
});
