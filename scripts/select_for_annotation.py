"""Selecciona un subset balanceado del dataset clasificacion para anotar en CVAT.

Lee `data/raw/public/mango-leaf-disease-cls/` (8 carpetas por enfermedad) y produce
`data/interim/cls-sampled-for-cvat/` con N imagenes por clase del catalogo MangoVision
mapeadas segun:

    Anthracnose       -> antracnosis     (target id 1)
    Healthy           -> sano            (target id 0)
    Powdery Mildew    -> oidio           (target id 2)
    Bacterial Canker  -> otras_lesiones  (target id 4)
    Cutting Weevil    -> otras_lesiones  (target id 4)
    Die Back          -> otras_lesiones  (target id 4)
    Gall Midge        -> otras_lesiones  (target id 4)
    Sooty Mould       -> otras_lesiones  (target id 4)

El dataset clasificacion **no incluye** `pudricion_peduncular` (id 3) — esa clase
se anota a partir de las capturas propias de Casma.

Las imagenes se renombran con prefijo de clase target para visualizacion clara en CVAT:
    sano__Healthy_001.jpg
    antracnosis__Anthracnose_001.jpg
    oidio__PowderyMildew_001.jpg
    otras_lesiones__BacterialCanker_001.jpg
    ...

Tambien genera `manifest.csv` con el mapeo original -> target para trazabilidad.

Uso:
    python scripts/select_for_annotation.py
    python scripts/select_for_annotation.py --per-class 50 --seed 7
    python scripts/select_for_annotation.py --output data/interim/sample-v2
"""
from __future__ import annotations

import argparse
import csv
import random
import shutil
from pathlib import Path

SOURCE_TO_TARGET = {
    "Anthracnose":       ("antracnosis", 1),
    "Healthy":           ("sano", 0),
    "Powdery Mildew":    ("oidio", 2),
    "Bacterial Canker":  ("otras_lesiones", 4),
    "Cutting Weevil":    ("otras_lesiones", 4),
    "Die Back":          ("otras_lesiones", 4),
    "Gall Midge":        ("otras_lesiones", 4),
    "Sooty Mould":       ("otras_lesiones", 4),
}

# Imagenes objetivo por clase target.
# "otras_lesiones" tiene 5 sub-fuentes, asi que distribuimos su cuota entre ellas.
DEFAULT_PER_TARGET = {
    "sano": 30,
    "antracnosis": 30,
    "oidio": 30,
    "otras_lesiones": 30,  # se reparte entre 5 sub-fuentes (6 c/u)
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/public/mango-leaf-disease-cls"),
        help="Carpeta del dataset clasificacion (8 sub-carpetas) (default: %(default)s)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path("data/interim/cls-sampled-for-cvat"),
        help="Carpeta destino (default: %(default)s)",
    )
    p.add_argument(
        "--per-class",
        type=int,
        default=30,
        help="Imagenes por clase target del catalogo (default: %(default)d). 'otras_lesiones' se reparte entre 5 sub-fuentes.",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed RNG para muestreo reproducible (default: %(default)d)",
    )
    return p.parse_args()


def sample_subfolder(folder: Path, count: int, rng: random.Random) -> list[Path]:
    images = sorted(
        p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS and p.is_file()
    )
    if len(images) < count:
        raise SystemExit(
            f"[ERROR] {folder.name} solo tiene {len(images)} imagenes, se piden {count}."
        )
    return rng.sample(images, count)


def slug(text: str) -> str:
    return text.replace(" ", "")


def main() -> int:
    args = parse_args()
    rng = random.Random(args.seed)

    if not args.source.is_dir():
        print(f"[ERROR] No existe la carpeta fuente: {args.source}")
        return 1

    if args.output.exists():
        print(f"[WARN] {args.output} ya existe; se limpiara.")
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)

    # Calcular cuantas imagenes tomar por sub-carpeta de la fuente.
    targets_count = {t: 0 for t in DEFAULT_PER_TARGET}
    for _src, (target, _id) in SOURCE_TO_TARGET.items():
        targets_count[target] = args.per_class

    per_subfolder: dict[str, int] = {}
    for target in targets_count:
        sources_for_target = [s for s, (t, _i) in SOURCE_TO_TARGET.items() if t == target]
        n_sources = len(sources_for_target)
        base = args.per_class // n_sources
        extra = args.per_class - base * n_sources
        for idx, src in enumerate(sources_for_target):
            per_subfolder[src] = base + (1 if idx < extra else 0)

    print(f"Plan de muestreo (seed={args.seed}, per_class={args.per_class}):")
    for src, n in per_subfolder.items():
        target_slug, target_id = SOURCE_TO_TARGET[src]
        print(f"  {src:18} -> {target_slug:16} (id {target_id})  : {n} imagenes")

    manifest_rows: list[dict] = []
    counters: dict[str, int] = {t: 1 for t in DEFAULT_PER_TARGET}

    for src_name, n in per_subfolder.items():
        src_dir = args.source / src_name
        if not src_dir.is_dir():
            print(f"[WARN] Carpeta no encontrada, se omite: {src_dir}")
            continue
        chosen = sample_subfolder(src_dir, n, rng)
        target_slug, target_id = SOURCE_TO_TARGET[src_name]
        for image_path in chosen:
            seq = counters[target_slug]
            counters[target_slug] += 1
            ext = image_path.suffix.lower()
            new_name = f"{target_slug}__{slug(src_name)}_{seq:03d}{ext}"
            dest = args.output / new_name
            shutil.copy2(image_path, dest)
            manifest_rows.append({
                "filename_in_sample": new_name,
                "original_filename": image_path.name,
                "original_class": src_name,
                "target_class": target_slug,
                "target_yolo_id": target_id,
            })

    manifest_path = args.output / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["filename_in_sample", "original_filename", "original_class", "target_class", "target_yolo_id"],
        )
        writer.writeheader()
        writer.writerows(manifest_rows)

    total = len(manifest_rows)
    print()
    print(f"[OK] {total} imagenes copiadas a {args.output}")
    print(f"     Manifest: {manifest_path}")
    print()
    print("Distribucion final por clase target:")
    for target in DEFAULT_PER_TARGET:
        c = sum(1 for r in manifest_rows if r["target_class"] == target)
        print(f"  {target:18}: {c}")
    print()
    print("Siguiente paso:")
    print(f"  1. Levantar CVAT (ver cvat/README.md)")
    print(f"  2. Crear task en CVAT, subir {args.output}")
    print(f"  3. Anotar bboxes reales (usa el prefijo del filename como hint de clase)")
    print(f"  4. Exportar a YOLO 1.1 -> data/raw/public/mango-leaf-disease-cls-annotated/labels/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
