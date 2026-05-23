import { render, type RenderOptions } from "@testing-library/react";
import type { ReactElement, ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";

import { AuthProvider } from "../hooks/AuthContext";

interface ProvidersProps {
  children: ReactNode;
  initialPath?: string;
}

function Providers({ children, initialPath = "/" }: ProvidersProps) {
  return (
    <MemoryRouter initialEntries={[initialPath]}>
      <AuthProvider>{children}</AuthProvider>
    </MemoryRouter>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options: Omit<RenderOptions, "wrapper"> & { initialPath?: string } = {},
) {
  const { initialPath, ...rest } = options;
  return render(ui, {
    wrapper: ({ children }) => <Providers initialPath={initialPath}>{children}</Providers>,
    ...rest,
  });
}
