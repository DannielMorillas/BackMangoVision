import { useEffect, useState } from "react";
import { ArrowRight, BarChart3, FileText, Globe, Leaf, ShieldCheck, Zap } from "lucide-react";
import { Link } from "react-router-dom";

import { Footer } from "../components/Footer";
import { Navbar } from "../components/Navbar";
import { DiseaseCard } from "../components/DiseaseCard";
import { fetchDiseases } from "../services/diseases";
import type { Disease } from "../types/disease";

export function LandingPage() {
  const [diseases, setDiseases] = useState<Disease[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDiseases()
      .then(setDiseases)
      .catch((err) => setError(err.message ?? "No se pudo cargar el catálogo"));
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-surface">
      <Navbar />

      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden pt-16 pb-24 lg:pt-24 lg:pb-32">
          <div className="absolute top-[-20%] right-[-10%] w-[50%] h-[60%] rounded-full bg-primary-100/60 blur-[120px] pointer-events-none" />
          <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[100px] pointer-events-none" />

          <div className="relative z-10 max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary-100 bg-primary-50 text-primary text-xs font-semibold uppercase tracking-wider mb-6">
                <span className="w-2 h-2 rounded-full bg-primary-light animate-pulse" />
                MangoVision · Deep Learning aplicado al agro
              </div>
              <h1 className="font-display text-4xl sm:text-5xl lg:text-[3.25rem] font-extrabold tracking-tight leading-[1.1] mb-6 text-text-primary">
                Diagnostica enfermedades del mango Kent en{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary-light">
                  segundos
                </span>
              </h1>
              <p className="text-lg text-text-muted mb-10 leading-relaxed max-w-xl">
                Sistema de reconocimiento automático de antracnosis, oídio y otras
                patologías mediante modelos YOLOv8 y U-Net entrenados con datos de
                ARA Export S.A.C.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/login"
                  data-testid="cta-primary-login"
                  className="px-8 py-4 rounded-xl bg-primary hover:bg-primary-light text-white font-semibold text-lg flex items-center justify-center gap-2 transition-all hover:shadow-lg hover:shadow-primary/20 hover:-translate-y-0.5"
                >
                  Iniciar sesión
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <a
                  href="#beneficios"
                  className="px-8 py-4 rounded-xl border border-border bg-white hover:bg-surface-alt text-text-primary font-semibold text-lg flex items-center justify-center transition-colors"
                >
                  Conocer más
                </a>
              </div>
            </div>

            <div className="hidden lg:block relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-primary-50 to-accent/5 blur-3xl rounded-full" />
              <div className="relative bg-white rounded-2xl card-shadow-lg border border-border overflow-hidden">
                <div className="bg-surface-alt border-b border-border p-3 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-400" />
                    <div className="w-3 h-3 rounded-full bg-yellow-400" />
                    <div className="w-3 h-3 rounded-full bg-green-400" />
                  </div>
                  <div className="mx-auto bg-white border border-border rounded-md px-4 py-1 text-[10px] text-text-muted font-mono">
                    mangovision.local / dashboard
                  </div>
                </div>
                <div className="p-5 space-y-4">
                  <div className="grid grid-cols-3 gap-3">
                    <div className="bg-primary-50 border border-primary-100 rounded-lg p-3">
                      <p className="text-[10px] text-primary/70 uppercase font-semibold mb-1">
                        Sano
                      </p>
                      <p className="text-xl font-bold text-primary">87%</p>
                    </div>
                    <div className="bg-amber-50 border border-amber-100 rounded-lg p-3">
                      <p className="text-[10px] text-amber-700/70 uppercase font-semibold mb-1">
                        Sospechoso
                      </p>
                      <p className="text-xl font-bold text-amber-700">9%</p>
                    </div>
                    <div className="bg-red-50 border border-red-100 rounded-lg p-3">
                      <p className="text-[10px] text-red-700/70 uppercase font-semibold mb-1">
                        Enfermo
                      </p>
                      <p className="text-xl font-bold text-red-700">4%</p>
                    </div>
                  </div>
                  <div className="rounded-xl border border-border p-4 flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary-50 rounded-full flex items-center justify-center">
                      <BarChart3 className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-xs text-text-muted uppercase font-semibold">
                        Lote AR-2026-042
                      </p>
                      <p className="text-sm font-semibold text-text-primary">
                        452 frutos analizados · 5.2 s
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Beneficios */}
        <section
          id="beneficios"
          className="py-24 px-6 max-w-7xl mx-auto w-full"
          aria-labelledby="beneficios-titulo"
        >
          <p className="text-sm font-bold text-primary uppercase tracking-wider mb-3">
            ¿Por qué MangoVision?
          </p>
          <h2
            id="beneficios-titulo"
            className="font-display text-3xl lg:text-4xl font-bold mb-12 max-w-3xl text-text-primary"
          >
            Diagnóstico fitosanitario sistemático para los lotes de exportación
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            <article className="benefit-card flex flex-col gap-3 p-6 rounded-2xl border border-border bg-white card-shadow">
              <div className="w-12 h-12 rounded-xl bg-primary-50 border border-primary-100 flex items-center justify-center">
                <Zap className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-bold text-text-primary">Detección rápida</h3>
              <p className="text-sm text-text-muted">
                Inferencia en menos de 5 segundos por imagen sobre modelo YOLOv8
                entrenado con datos propios.
              </p>
            </article>

            <article className="benefit-card flex flex-col gap-3 p-6 rounded-2xl border border-border bg-white card-shadow">
              <div className="w-12 h-12 rounded-xl bg-amber-50 border border-amber-100 flex items-center justify-center">
                <FileText className="w-6 h-6 text-amber-600" />
              </div>
              <h3 className="text-lg font-bold text-text-primary">
                Trazabilidad por lote
              </h3>
              <p className="text-sm text-text-muted">
                Cada diagnóstico queda registrado con lote y parcela, listo para
                auditoría SENASA y GlobalGAP.
              </p>
            </article>

            <article className="benefit-card flex flex-col gap-3 p-6 rounded-2xl border border-border bg-white card-shadow">
              <div className="w-12 h-12 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center">
                <Globe className="w-6 h-6 text-blue-500" />
              </div>
              <h3 className="text-lg font-bold text-text-primary">
                Exportable a mercados exigentes
              </h3>
              <p className="text-sm text-text-muted">
                Salida de bounding boxes, severidad y porcentaje de área afectada
                alineada con estándares fitosanitarios.
              </p>
            </article>
          </div>
        </section>

        {/* Enfermedades */}
        <section
          id="enfermedades"
          className="py-24 px-6 bg-surface-alt border-y border-border"
          aria-labelledby="enfermedades-titulo"
        >
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <p className="text-sm font-bold text-primary uppercase tracking-wider mb-3">
                Catálogo
              </p>
              <h2
                id="enfermedades-titulo"
                className="font-display text-3xl lg:text-4xl font-bold text-text-primary"
              >
                Enfermedades detectables
              </h2>
            </div>

            {error && (
              <p
                role="alert"
                className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-4 max-w-xl mx-auto text-center"
              >
                {error}
              </p>
            )}

            {!diseases && !error && (
              <p data-testid="diseases-loading" className="text-center text-text-muted">
                Cargando catálogo…
              </p>
            )}

            {diseases && (
              <div className="grid md:grid-cols-3 gap-6">
                {diseases.map((disease) => (
                  <DiseaseCard key={disease.slug} disease={disease} />
                ))}
              </div>
            )}
          </div>
        </section>

        {/* CTA Final */}
        <section className="relative py-24 px-6 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-amber-50/30" />
          <div className="relative z-10 max-w-3xl mx-auto text-center">
            <div className="w-16 h-16 mx-auto bg-gradient-to-br from-primary to-primary-light rounded-2xl flex items-center justify-center shadow-lg shadow-primary/20 mb-6">
              <ShieldCheck className="w-8 h-8 text-white" />
            </div>
            <h2 className="font-display text-3xl lg:text-5xl font-bold mb-6 text-text-primary">
              ¿Listo para empezar?
            </h2>
            <p className="text-lg text-text-muted mb-8">
              Inicia sesión con tu cuenta de ingeniero agrónomo de ARA Export S.A.C. y
              empieza a analizar tus primeros lotes.
            </p>
            <Link
              to="/login"
              className="inline-flex items-center gap-3 px-10 py-4 rounded-2xl bg-primary hover:bg-primary-light text-white font-bold text-lg transition-all hover:shadow-lg hover:shadow-primary/20 hover:-translate-y-0.5"
            >
              <Leaf className="w-5 h-5" />
              Iniciar sesión
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
