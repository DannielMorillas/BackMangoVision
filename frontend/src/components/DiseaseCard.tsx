import type { Disease } from "../types/disease";

interface Props {
  disease: Disease;
}

export function DiseaseCard({ disease }: Props) {
  return (
    <article
      data-testid="disease-card"
      data-slug={disease.slug}
      className="bg-white p-6 rounded-2xl border border-border card-shadow hover:card-shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col items-start"
    >
      <span
        className="w-3 h-3 rounded-full mb-4"
        style={{ backgroundColor: disease.color_hex }}
        aria-hidden="true"
      />
      <span
        className="text-xs font-bold uppercase tracking-wider mb-2 px-2 py-1 rounded-md"
        style={{
          color: disease.color_hex,
          backgroundColor: `${disease.color_hex}15`,
        }}
      >
        {disease.name}
      </span>
      <p className="text-sm text-text-muted leading-relaxed">{disease.description}</p>
    </article>
  );
}
