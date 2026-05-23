import { ArrowLeft, Leaf } from "lucide-react";
import { Link } from "react-router-dom";

export function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center bg-surface-alt py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <Link
        to="/"
        className="absolute top-6 left-6 flex items-center gap-2 text-text-muted hover:text-primary transition-colors z-20 font-medium"
      >
        <ArrowLeft className="w-5 h-5" />
        <span className="hidden sm:inline">Volver</span>
      </Link>

      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-100/40 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[100px] pointer-events-none" />

      <div className="relative z-10 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-primary-light flex items-center justify-center shadow-lg shadow-primary/20">
            <Leaf className="w-8 h-8 text-white" />
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-text-primary font-display">
          MangoVision
        </h2>
        <p className="mt-2 text-center text-sm text-text-muted">
          Sistema de diagnóstico fitosanitario · ARA Export S.A.C.
        </p>
      </div>

      <div className="relative z-10 mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-lg shadow-black/5 sm:rounded-2xl sm:px-10 border border-border text-center">
          <p className="text-text-muted text-sm">
            Formulario de inicio de sesión en construcción (HU-004).
          </p>
        </div>
      </div>
    </div>
  );
}
