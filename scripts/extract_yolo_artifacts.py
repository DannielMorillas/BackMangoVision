"""Extrae los artefactos relevantes de un run de YOLOv8 a una carpeta de evidencias del sprint.

Cuando entrenas con Ultralytics (`yolo train ...`), el output queda en:
    runs/detect/train/
    ├── weights/{best.pt, last.pt}
    ├── results.csv              <- metricas por epoca
    ├── results.png              <- graficos de loss / mAP / lr
    ├── PR_curve.png             <- curva precision-recall
    ├── F1_curve.png             <- curva F1 vs confidence
    ├── P_curve.png              <- precision vs confidence
    ├── R_curve.png              <- recall vs confidence
    ├── confusion_matrix.png
    ├── confusion_matrix_normalized.png
    ├── labels.jpg               <- distribucion del dataset
    ├── labels_correlogram.jpg
    ├── train_batch*.jpg         <- ejemplos de batches con augmentation
    ├── val_batch*_labels.jpg    <- ground truth val
    └── val_batch*_pred.jpg      <- predicciones val

Este script copia los graficos clave (results.png, PR_curve.png, etc.) a:
    docs/sprints/sprint-3/evidencias/screenshots/<run-tag>/

Y extrae las metricas finales del results.csv generando:
    docs/sprints/sprint-3/evidencias/screenshots/<run-tag>/SUMMARY.md

Uso:
    python scripts/extract_yolo_artifacts.py --run-dir ml/runs/detect/train --tag baseline-v0
    python scripts/extract_yolo_artifacts.py --run-dir ml/runs/detect/train2 --tag final-v1
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

# La consola de Windows (cp1252) no puede imprimir los simbolos ✓/✅ que usa este
# script y aborta con UnicodeEncodeError. Forzamos UTF-8 en stdout cuando se pueda.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
except Exception:
    pass

# Graficos clave (en orden de importancia para evidencia)
# Las versiones nuevas de Ultralytics prefijan las curvas con "Box" (BoxPR_curve.png,
# BoxF1_curve.png, ...). Incluimos ambos nombres; solo se copia el que exista en el run.
CORE_PLOTS = [
    "results.png",
    "PR_curve.png",
    "BoxPR_curve.png",
    "F1_curve.png",
    "BoxF1_curve.png",
    "P_curve.png",
    "BoxP_curve.png",
    "R_curve.png",
    "BoxR_curve.png",
    "confusion_matrix.png",
    "confusion_matrix_normalized.png",
    "labels.jpg",
    "labels_correlogram.jpg",
]
# Si existen, se copian tambien
OPTIONAL_FILES = ["results.csv", "args.yaml", "events.out.tfevents.*"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--run-dir",
        type=Path,
        required=True,
        help="Carpeta del run de YOLO (ej: ml/runs/detect/train)",
    )
    p.add_argument(
        "--tag",
        type=str,
        required=True,
        help="Nombre corto del run (ej: baseline-v0, custom-v1) — se usa como subcarpeta destino",
    )
    p.add_argument(
        "--output-base",
        type=Path,
        default=Path("docs/sprints/sprint-3/evidencias/screenshots"),
        help="Carpeta destino (default: %(default)s)",
    )
    p.add_argument(
        "--include-batches",
        action="store_true",
        help="Tambien copia los train_batch*.jpg y val_batch*.jpg (varios MB)",
    )
    return p.parse_args()


def read_final_metrics(results_csv: Path) -> dict[str, str]:
    """Lee la ultima fila de results.csv y devuelve un dict de metricas."""
    if not results_csv.is_file():
        return {}
    with results_csv.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        last_row: dict | None = None
        for row in reader:
            last_row = row
    if last_row is None:
        return {}
    return {k.strip(): v.strip() for k, v in last_row.items()}


def find_best_epoch(results_csv: Path) -> tuple[int | None, dict[str, str]]:
    """Encuentra la epoca con mejor mAP@0.5 y devuelve (epoca, fila)."""
    if not results_csv.is_file():
        return None, {}
    best_map = -1.0
    best_row: dict[str, str] | None = None
    best_epoch: int | None = None
    with results_csv.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # busca columnas tipicas de YOLOv8: 'metrics/mAP50(B)' o 'metrics/mAP_0.5'
            for key in row:
                if "mAP50" in key and "95" not in key:
                    try:
                        val = float(row[key])
                        if val > best_map:
                            best_map = val
                            best_row = {k.strip(): v.strip() for k, v in row.items()}
                            try:
                                best_epoch = int(row.get("epoch", "-1").strip())
                            except ValueError:
                                best_epoch = None
                    except ValueError:
                        pass
                    break
    return best_epoch, best_row or {}


def render_summary(tag: str, run_dir: Path, copied: list[str], final: dict, best_epoch: int | None, best: dict) -> str:
    lines = [
        f"# Resumen de run YOLO — `{tag}`",
        "",
        f"**Carpeta origen:** `{run_dir}`",
        f"**Fecha de extracción:** generada automáticamente por `scripts/extract_yolo_artifacts.py`",
        "",
        "## Archivos copiados",
        "",
    ]
    for name in copied:
        lines.append(f"- `{name}`")
    lines.append("")

    if final:
        lines.extend([
            "## Métricas de la última época",
            "",
            "| Métrica | Valor |",
            "|---|---|",
        ])
        priority_keys = [
            "epoch",
            "train/box_loss",
            "train/cls_loss",
            "train/dfl_loss",
            "val/box_loss",
            "val/cls_loss",
            "val/dfl_loss",
            "metrics/precision(B)",
            "metrics/recall(B)",
            "metrics/mAP50(B)",
            "metrics/mAP50-95(B)",
            "lr/pg0",
        ]
        shown_keys = set()
        for key in priority_keys:
            if key in final:
                lines.append(f"| `{key}` | {final[key]} |")
                shown_keys.add(key)
        # Resto de metricas
        for key, val in final.items():
            if key in shown_keys:
                continue
            lines.append(f"| `{key}` | {val} |")
        lines.append("")

    if best_row := best:
        lines.extend([
            f"## Mejor época por `mAP@0.5` (epoch {best_epoch if best_epoch is not None else '?'})",
            "",
            "| Métrica | Valor |",
            "|---|---|",
        ])
        for key, val in best_row.items():
            lines.append(f"| `{key}` | {val} |")
        lines.append("")

    lines.extend([
        "## Cómo se cumple RN-001",
        "",
        "RN-001 exige `mAP@0.5 ≥ 0.85` en el test set. La métrica `metrics/mAP50(B)` de la mejor época indica",
        "el desempeño en el set de **validación** durante el training. Para la verificación final en el set de",
        "**test**, ejecutar:",
        "",
        "```powershell",
        "yolo val data=data/processed/dataset.yaml model=ml/models/best.pt split=test",
        "```",
        "",
        "El número de `mAP50` reportado por ese comando es el que cuenta para cerrar RN-001.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if not args.run_dir.is_dir():
        print(f"[ERROR] No existe la carpeta run: {args.run_dir}")
        return 1

    dest = args.output_base / args.tag
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Extrayendo desde: {args.run_dir}")
    print(f"Destino:          {dest}")
    print()

    copied: list[str] = []
    # Plots principales
    for name in CORE_PLOTS:
        src = args.run_dir / name
        if src.is_file():
            shutil.copy2(src, dest / name)
            copied.append(name)
            print(f"  ✓ {name}")
        else:
            print(f"  - {name} (no existe en el run)")

    # results.csv
    csv_path = args.run_dir / "results.csv"
    if csv_path.is_file():
        shutil.copy2(csv_path, dest / "results.csv")
        copied.append("results.csv")
        print(f"  ✓ results.csv")

    # args.yaml (config del training)
    args_yaml = args.run_dir / "args.yaml"
    if args_yaml.is_file():
        shutil.copy2(args_yaml, dest / "args.yaml")
        copied.append("args.yaml")
        print(f"  ✓ args.yaml")

    # Batches opcionales
    if args.include_batches:
        for pattern in ("train_batch*.jpg", "val_batch*_labels.jpg", "val_batch*_pred.jpg"):
            for src in args.run_dir.glob(pattern):
                shutil.copy2(src, dest / src.name)
                copied.append(src.name)
                print(f"  ✓ {src.name}")

    # Metricas
    final = read_final_metrics(csv_path)
    best_epoch, best = find_best_epoch(csv_path)
    summary = render_summary(args.tag, args.run_dir, copied, final, best_epoch, best)
    summary_path = dest / "SUMMARY.md"
    summary_path.write_text(summary, encoding="utf-8")
    copied.append("SUMMARY.md")
    print(f"  ✓ SUMMARY.md (generado)")

    print()
    print(f"[OK] {len(copied)} archivos en {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
