"""Verifica que un dataset en formato YOLO esté íntegro y mapeado a nuestro catálogo.

Uso:
    python scripts/verify_yolo_dataset.py data/raw/public
    python scripts/verify_yolo_dataset.py data/raw/aragroexport

Verifica:
    1. Estructura: existen carpetas `images/` y `labels/`.
    2. Cada imagen tiene su archivo .txt correspondiente (mismo basename).
    3. Cada label tiene su imagen correspondiente (sin huérfanos).
    4. Los IDs de clase están en el rango [0..4] (nuestras 5 clases).
    5. Las coordenadas YOLO están normalizadas en [0..1].

Reporta:
    - Conteo total de imágenes y labels.
    - Distribución de bounding boxes por clase.
    - Inconsistencias.

Exit code: 0 si todo OK, 1 si encuentra problemas.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

CLASS_NAMES = [
    "sano",
    "antracnosis",
    "oidio",
    "pudricion_peduncular",
    "otras_lesiones",
]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def list_basenames(path: Path, extensions: set[str]) -> set[str]:
    return {p.stem for p in path.iterdir() if p.suffix.lower() in extensions and p.is_file()}


def parse_label_file(path: Path) -> tuple[list[int], list[str]]:
    """Devuelve (class_ids, problemas) por archivo."""
    class_ids: list[int] = []
    problems: list[str] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 5:
            problems.append(f"{path.name}:{lineno}: esperadas 5 columnas (class x y w h), encontradas {len(parts)}")
            continue
        try:
            class_id = int(parts[0])
            x, y, w, h = (float(v) for v in parts[1:])
        except ValueError as e:
            problems.append(f"{path.name}:{lineno}: no parseable ({e})")
            continue
        if class_id < 0 or class_id >= len(CLASS_NAMES):
            problems.append(
                f"{path.name}:{lineno}: class_id={class_id} fuera de rango [0..{len(CLASS_NAMES) - 1}]"
            )
        for name, val in (("x", x), ("y", y), ("w", w), ("h", h)):
            if not (0.0 <= val <= 1.0):
                problems.append(f"{path.name}:{lineno}: {name}={val} no normalizado en [0..1]")
        class_ids.append(class_id)
    return class_ids, problems


def verify(dataset_root: Path) -> int:
    images_dir = dataset_root / "images"
    labels_dir = dataset_root / "labels"

    if not images_dir.is_dir() or not labels_dir.is_dir():
        print(f"[ERROR] Estructura esperada: {dataset_root}/{{images,labels}}/")
        return 1

    img_basenames = list_basenames(images_dir, IMAGE_EXTS)
    lbl_basenames = list_basenames(labels_dir, {".txt"})

    print(f"Dataset: {dataset_root}")
    print(f"  imágenes : {len(img_basenames)}")
    print(f"  labels   : {len(lbl_basenames)}")

    missing_labels = sorted(img_basenames - lbl_basenames)
    orphan_labels = sorted(lbl_basenames - img_basenames)

    has_issues = False

    if missing_labels:
        has_issues = True
        print(f"  [!] Imágenes sin label ({len(missing_labels)}):")
        for name in missing_labels[:10]:
            print(f"      - {name}")
        if len(missing_labels) > 10:
            print(f"      ... y {len(missing_labels) - 10} más")

    if orphan_labels:
        has_issues = True
        print(f"  [!] Labels sin imagen ({len(orphan_labels)}):")
        for name in orphan_labels[:10]:
            print(f"      - {name}")

    class_counts: Counter[int] = Counter()
    all_problems: list[str] = []
    for label_path in labels_dir.glob("*.txt"):
        class_ids, problems = parse_label_file(label_path)
        class_counts.update(class_ids)
        all_problems.extend(problems)

    print("\n  Distribución de bounding boxes por clase:")
    for cid, name in enumerate(CLASS_NAMES):
        count = class_counts.get(cid, 0)
        bar = "█" * min(40, count // max(1, max(class_counts.values()) // 40)) if class_counts else ""
        print(f"    {cid} {name:25} {count:6}  {bar}")

    out_of_range = sum(c for cid, c in class_counts.items() if cid >= len(CLASS_NAMES) or cid < 0)
    if out_of_range:
        has_issues = True
        print(f"  [!] {out_of_range} bounding boxes con class_id fuera de rango")

    if all_problems:
        has_issues = True
        print(f"\n  [!] {len(all_problems)} líneas con problemas de formato:")
        for problem in all_problems[:20]:
            print(f"      - {problem}")
        if len(all_problems) > 20:
            print(f"      ... y {len(all_problems) - 20} más")

    if has_issues:
        print("\n[FAIL] Se encontraron inconsistencias. Revisar arriba.")
        return 1

    total_boxes = sum(class_counts.values())
    print(f"\n[OK] Dataset íntegro. Total bounding boxes: {total_boxes}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica un dataset YOLO de MangoVision.")
    parser.add_argument(
        "dataset_root",
        type=Path,
        help="Ruta a la carpeta del dataset (debe contener images/ y labels/).",
    )
    args = parser.parse_args()
    return verify(args.dataset_root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
