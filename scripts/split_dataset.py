"""Divide el dataset hibrido (publico anotado + Casma) en train/val/test estratificado.

Lee pares (image, label) de uno o mas directorios fuente que sigan la estructura:
    <source>/images/<archivo>.jpg
    <source>/labels/<archivo>.txt    (formato YOLO; mismo basename que la imagen)

Para cada par calcula la *clase dominante* (la mas frecuente entre los bboxes del archivo).
Luego para cada clase aplica un split estratificado segun los ratios indicados.

Genera la estructura final consumible por YOLOv8:
    data/processed/
    ├── train/{images,labels}/
    ├── val/{images,labels}/
    ├── test/{images,labels}/
    ├── dataset.yaml           ← generado al final (EN-004)
    └── split-manifest.csv     ← traza qué archivo fue a qué split

Uso:
    python scripts/split_dataset.py                              # defaults
    python scripts/split_dataset.py --seed 7 --ratios 0.8 0.1 0.1
    python scripts/split_dataset.py \\
        --source data/raw/aragroexport \\
        --source data/raw/public/mango-leaf-disease-cls-annotated
"""
from __future__ import annotations

import argparse
import csv
import random
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

CLASS_NAMES = [
    "sano",
    "antracnosis",
    "oidio",
    "pudricion_peduncular",
    "otras_lesiones",
]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--source",
        action="append",
        type=Path,
        default=None,
        help=(
            "Carpeta(s) fuente con sub-estructura images/ + labels/. "
            "Se puede pasar varias veces. Default: "
            "['data/raw/aragroexport', 'data/raw/public/mango-leaf-disease-cls-annotated']."
        ),
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed"),
        help="Carpeta destino (default: %(default)s)",
    )
    p.add_argument(
        "--ratios",
        nargs=3,
        type=float,
        default=[0.7, 0.15, 0.15],
        metavar=("TRAIN", "VAL", "TEST"),
        help="Proporcion train/val/test (default: %(default)s)",
    )
    p.add_argument("--seed", type=int, default=42, help="Seed RNG (default: %(default)d)")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="No copia archivos; solo reporta lo que haria.",
    )
    args = p.parse_args()
    if args.source is None:
        args.source = [
            Path("data/raw/aragroexport"),
            Path("data/raw/public/mango-leaf-disease-cls-annotated"),
        ]
    if abs(sum(args.ratios) - 1.0) > 1e-6:
        p.error(f"--ratios debe sumar 1.0, recibido {sum(args.ratios)}")
    return args


def dominant_class(label_path: Path) -> int | None:
    """Devuelve el class_id mas frecuente en el archivo de label. None si vacio o invalido."""
    if not label_path.is_file():
        return None
    counts: Counter[int] = Counter()
    text = label_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            cid = int(line.split()[0])
        except (ValueError, IndexError):
            continue
        if 0 <= cid < len(CLASS_NAMES):
            counts[cid] += 1
    if not counts:
        return None
    return counts.most_common(1)[0][0]


def collect_pairs(sources: list[Path]) -> list[tuple[Path, Path, int]]:
    """Devuelve lista de (image_path, label_path, dominant_class_id) para todos los pares validos."""
    pairs: list[tuple[Path, Path, int]] = []
    for source in sources:
        images_dir = source / "images"
        labels_dir = source / "labels"
        if not images_dir.is_dir() or not labels_dir.is_dir():
            print(f"[WARN] {source} no tiene images/ o labels/, se omite.")
            continue
        found_in_source = 0
        for img_path in sorted(images_dir.rglob("*")):
            if not img_path.is_file() or img_path.suffix.lower() not in IMAGE_EXTS:
                continue
            label_path = labels_dir / f"{img_path.stem}.txt"
            cls = dominant_class(label_path)
            if cls is None:
                continue
            pairs.append((img_path, label_path, cls))
            found_in_source += 1
        print(f"  {source}: {found_in_source} pares utiles")
    return pairs


def split_per_class(
    pairs: list[tuple[Path, Path, int]],
    ratios: list[float],
    rng: random.Random,
) -> dict[str, list[tuple[Path, Path, int]]]:
    """Devuelve dict con keys 'train','val','test' aplicando split estratificado por clase."""
    by_class: dict[int, list[tuple[Path, Path, int]]] = defaultdict(list)
    for p in pairs:
        by_class[p[2]].append(p)

    splits: dict[str, list[tuple[Path, Path, int]]] = {"train": [], "val": [], "test": []}
    for cls, group in by_class.items():
        rng.shuffle(group)
        n = len(group)
        n_train = int(round(n * ratios[0]))
        n_val = int(round(n * ratios[1]))
        # Para evitar perder muestras por redondeo, test se queda con el resto.
        n_test = n - n_train - n_val
        if n_train + n_val + n_test != n or any(x < 0 for x in (n_train, n_val, n_test)):
            raise SystemExit(
                f"[ERROR] split inconsistente para clase {cls}: {n_train}/{n_val}/{n_test} sobre {n}"
            )
        splits["train"].extend(group[:n_train])
        splits["val"].extend(group[n_train : n_train + n_val])
        splits["test"].extend(group[n_train + n_val :])
    return splits


def report_distribution(splits: dict[str, list[tuple[Path, Path, int]]]) -> None:
    """Imprime un cuadro distribucion split x clase."""
    print()
    print(f"{'Split':<8} | " + " | ".join(f"{n[:6]:>6}" for n in CLASS_NAMES) + " | TOTAL")
    print("-" * 70)
    for split in ("train", "val", "test"):
        counts = Counter(cls for _, _, cls in splits[split])
        cells = [counts.get(i, 0) for i in range(len(CLASS_NAMES))]
        print(f"{split:<8} | " + " | ".join(f"{c:>6}" for c in cells) + f" | {sum(cells):>5}")
    print("-" * 70)


def copy_to_output(
    splits: dict[str, list[tuple[Path, Path, int]]],
    output: Path,
    dry_run: bool,
) -> list[dict]:
    """Copia pares al destino y devuelve filas de manifest."""
    manifest_rows: list[dict] = []
    for split, items in splits.items():
        img_dir = output / split / "images"
        lbl_dir = output / split / "labels"
        if not dry_run:
            img_dir.mkdir(parents=True, exist_ok=True)
            lbl_dir.mkdir(parents=True, exist_ok=True)
        for img_path, lbl_path, cls in items:
            dest_img = img_dir / img_path.name
            dest_lbl = lbl_dir / lbl_path.name
            if not dry_run:
                shutil.copy2(img_path, dest_img)
                shutil.copy2(lbl_path, dest_lbl)
            manifest_rows.append(
                {
                    "split": split,
                    "image": str(img_path),
                    "label": str(lbl_path),
                    "dominant_class_id": cls,
                    "dominant_class_name": CLASS_NAMES[cls],
                }
            )
    return manifest_rows


def write_manifest(rows: list[dict], output: Path, dry_run: bool) -> None:
    if dry_run:
        return
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "split-manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["split", "image", "label", "dominant_class_id", "dominant_class_name"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Manifest: {manifest_path}")


def write_dataset_yaml(output: Path, dry_run: bool) -> None:
    """Genera el dataset.yaml de YOLOv8 con paths absolutos."""
    if dry_run:
        return
    abs_path = output.resolve()
    lines = [
        f"# Generado por scripts/split_dataset.py",
        f"# No editar a mano: re-ejecutar el split para regenerar.",
        f"",
        f"path: {abs_path.as_posix()}",
        f"train: train/images",
        f"val: val/images",
        f"test: test/images",
        f"",
        f"nc: {len(CLASS_NAMES)}",
        f"names:",
    ]
    for i, name in enumerate(CLASS_NAMES):
        lines.append(f"  {i}: {name}")
    yaml_path = output / "dataset.yaml"
    yaml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"dataset.yaml: {yaml_path}")


def main() -> int:
    args = parse_args()
    print(f"Sources:")
    for s in args.source:
        print(f"  - {s}")
    print(f"Output: {args.output}")
    print(f"Ratios: train={args.ratios[0]} val={args.ratios[1]} test={args.ratios[2]}")
    print(f"Seed:   {args.seed}")
    print(f"Dry-run: {args.dry_run}")
    print()
    print("Recolectando pares (image, label)...")
    pairs = collect_pairs(args.source)
    if not pairs:
        print()
        print("[INFO] 0 pares encontrados — todavia no hay datos anotados.")
        print("       Este script estara listo para correr cuando exista:")
        print("       1) data/raw/aragroexport/{images,labels}/  (fotos Casma + anotaciones CVAT)")
        print("       2) data/raw/public/mango-leaf-disease-cls-annotated/{images,labels}/  (export CVAT)")
        return 0
    print(f"  Total: {len(pairs)} pares")

    rng = random.Random(args.seed)
    splits = split_per_class(pairs, args.ratios, rng)
    report_distribution(splits)

    if args.output.exists() and not args.dry_run:
        print(f"\n[WARN] {args.output} ya existe; sub-carpetas split se sobre-escribiran.")
        for sub in ("train", "val", "test"):
            sub_path = args.output / sub
            if sub_path.exists():
                shutil.rmtree(sub_path)

    print()
    print(f"Copiando archivos ({'dry-run' if args.dry_run else 'real'})...")
    rows = copy_to_output(splits, args.output, args.dry_run)
    write_manifest(rows, args.output, args.dry_run)
    write_dataset_yaml(args.output, args.dry_run)
    print()
    print(f"[OK] Split completado: {len(rows)} pares distribuidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
