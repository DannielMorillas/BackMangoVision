import { LayoutDashboard, Leaf, LogIn } from "lucide-react";
import { Link } from "react-router-dom";

import { useAuth } from "../hooks/AuthContext";

export function Navbar() {
  const { status, user } = useAuth();
  const isAuthenticated = status === "authenticated" && user;

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-border px-6 py-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-primary-light flex items-center justify-center">
            <Leaf className="w-5 h-5 text-white" />
          </div>
          <span className="font-display font-bold text-xl tracking-tight text-text-primary">
            MangoVision
          </span>
        </Link>
        <div className="flex items-center gap-3 text-sm font-medium">
          <a
            href="#beneficios"
            className="hidden md:inline text-text-muted hover:text-primary transition-colors px-3 py-2"
          >
            Beneficios
          </a>
          <a
            href="#enfermedades"
            className="hidden md:inline text-text-muted hover:text-primary transition-colors px-3 py-2"
          >
            Enfermedades
          </a>
          {isAuthenticated ? (
            <Link
              to="/dashboard"
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary text-white hover:bg-primary-light transition-colors font-medium text-sm shadow-sm"
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </Link>
          ) : (
            <Link
              to="/login"
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary text-white hover:bg-primary-light transition-colors font-medium text-sm shadow-sm"
            >
              <LogIn className="w-4 h-4" />
              <span>Iniciar sesión</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
