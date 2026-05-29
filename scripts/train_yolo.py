"""Entrena un modelo YOLOv8 sobre nuestro dataset_yaml.

Wrapper minimo sobre `ultralytics.YOLO(...).train(...)` con argumentos del proyecto:

    EN-005 (baseline con datos publicos):
        python scripts/train_yolo.py --tag baseline-v0 --data data/raw/public/mango-v1-yolov8/data.yaml --epochs 50

    EN-006 (modelo final con dataset hibrido):
        python scripts/train_yolo.py --tag custom-v1 --data data/processed/dataset.yaml --epochs 100 \\
            --resume-from ml/models/baseline-v0.pt

Despues del training, extrae automaticamente los artefactos a docs/sprints/sprint-3/evidencias/screenshots/<tag>/

Requisitos:
    pip install ultralytics
    # GPU recomendada (CUDA 11.8+ o MPS en Mac). En CPU el training tarda mucho.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None  # type: ignore


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tag", required=True, help="Identificador del run (ej: baseline-v0, custom-v1)")
    p.add_argument("--data", type=Path, required=True, help="Path al dataset.yaml")
    p.add_argument(
        "--model",
        default="yolov8n.pt",
        help="Pesos iniciales (default: %(default)s). 'yolov8n.pt' es el mas chico; 'yolov8s.pt', 'yolov8m.pt' son progresivamente mas grandes.",
    )
    p.add_argument("--epochs", type=int, default=50, help="Numero de epocas (default: %(default)d)")
    p.add_argument("--imgsz", type=int, default=640, help="Tamano de imagen (default: %(default)d)")
    p.add_argument("--batch", type=int, default=16, help="Batch size (default: %(default)d). Reducir si OOM.")
    p.add_argument(
        "--device",
        default="0",
        help="Device YOLO: '0' (GPU CUDA), 'cpu', 'mps' (Mac). Default: %(default)s",
    )
    p.add_argument(
        "--project",
        type=Path,
        default=Path("ml/runs"),
        help="Carpeta donde YOLO crea sub-carpetas detect/train/ (default: %(default)s)",
    )
    p.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="Path a un .pt existente para continuar training (transfer learning entre EN-005 y EN-006)",
    )
    p.add_argument(
        "--skip-extract",
        action="store_true",
        help="No ejecutar extract_yolo_artifacts.py al final",
    )
    p.add_argument(
        "--include-batches",
        action="store_true",
        help="Incluir batches en la extraccion (pesado)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if YOLO is None:
        print("[ERROR] ultralytics no esta instalado. Ejecuta: pip install ultralytics")
        return 1

    initial_model = args.resume_from if args.resume_from else args.model
    print(f"Entrenando {args.tag}")
    print(f"  Dataset:  {args.data}")
    print(f"  Modelo:   {initial_model}")
    print(f"  Epochs:   {args.epochs}")
    print(f"  Img size: {args.imgsz}")
    print(f"  Batch:    {args.batch}")
    print(f"  Device:   {args.device}")
    print(f"  Salida:   {args.project}/detect/{args.tag}")
    print()

    model = YOLO(str(initial_model))
    results = model.train(
        data=str(args.data),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=str(args.project),
        name=args.tag,
        exist_ok=False,
        plots=True,
        save=True,
    )

    run_dir = args.project / "detect" / args.tag
    best_pt = run_dir / "weights" / "best.pt"
    if best_pt.is_file():
        # Tambien copiar el best.pt a ml/models/ con el tag para acceso rapido
        models_dir = Path("ml/models")
        models_dir.mkdir(parents=True, exist_ok=True)
        dest = models_dir / f"{args.tag}.pt"
        shutil.copy2(best_pt, dest)
        print(f"\n[OK] Modelo copiado a {dest}")

    if not args.skip_extract:
        print(f"\nExtrayendo artefactos...")
        extract_cmd = [
            sys.executable,
            "scripts/extract_yolo_artifacts.py",
            "--run-dir", str(run_dir),
            "--tag", args.tag,
        ]
        if args.include_batches:
            extract_cmd.append("--include-batches")
        subprocess.run(extract_cmd, check=False)

    print()
    print(f"[DONE] Training y extraccion completos para tag '{args.tag}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
