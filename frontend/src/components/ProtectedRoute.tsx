import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";
import type { UserRole } from "../types/user";

interface Props {
  children: ReactNode;
  requireRole?: UserRole;
}

export function ProtectedRoute({ children, requireRole }: Props) {
  const { status, user } = useAuth();
  const location = useLocation();

  if (status === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center text-text-muted">
        Cargando sesión…
      </div>
    );
  }

  if (status === "anonymous" || !user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (requireRole && user.role !== requireRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}
