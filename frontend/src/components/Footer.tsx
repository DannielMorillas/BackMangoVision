export function Footer() {
  return (
    <footer className="bg-text-primary text-white pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-3 gap-12 mb-12">
        <div>
          <p className="font-display font-bold text-xl mb-3">MangoVision</p>
          <p className="text-white/60 text-sm leading-relaxed">
            Diagnóstico fitosanitario asistido por Deep Learning para los frutos de
            mango Kent de ARA Export S.A.C.
          </p>
        </div>
        <div>
          <h4 className="font-bold mb-4 font-display">Producto</h4>
          <ul className="space-y-2 text-sm text-white/60">
            <li>
              <a href="#beneficios" className="hover:text-white transition-colors">
                Beneficios
              </a>
            </li>
            <li>
              <a href="#enfermedades" className="hover:text-white transition-colors">
                Enfermedades detectables
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="font-bold mb-4 font-display">Investigación</h4>
          <p className="text-sm text-white/60 mb-1">
            Universidad Privada Antenor Orrego
          </p>
          <p className="text-xs text-white/40">
            Facultad de Ingeniería · Trujillo, Perú
          </p>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 border-t border-white/10 pt-6 text-xs text-white/40 flex justify-between">
        <p>© {new Date().getFullYear()} ARA Export S.A.C.</p>
        <p>Versión 0.1 · Desarrollo</p>
      </div>
    </footer>
  );
}
