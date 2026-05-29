# `ml/` — Modelos IA y artefactos de entrenamiento

Esta carpeta aloja los notebooks, runs y modelos del Sprint 3 (Entrenamiento de Modelos IA).

> ⚠️ **Los artefactos pesados (runs, pesos .pt) no se versionan en Git.** Solo este README y los notebooks (`notebooks/*.ipynb`) viajan en el repo. Cada miembro entrena localmente o en Colab y comparte los gráficos de evidencia vía `extract_yolo_artifacts.py`.

## Estructura

```
ml/
├── README.md                ← este archivo (versionado)
├── notebooks/               ← notebooks Jupyter para training (versionado)
│   └── (vacio al inicio; se llena en EN-005/006/007)
├── models/                  ← gitignored — pesos finales .pt y .onnx
│   ├── baseline-v0.pt       (EN-005 — sera generado)
│   ├── custom-v1.pt         (EN-006 — sera generado)
│   └── unet-severity-v1.pt  (EN-007 — sera generado)
└── runs/                    ← gitignored — outputs de YOLOv8
    └── detect/
        └── <tag>/
            ├── weights/{best.pt, last.pt}
            ├── results.png
            ├── PR_curve.png
            └── ...
```

## Workflows del Sprint 3

### EN-005 — Baseline con datos públicos

```powershell
# Entrenar (CPU lento, GPU recomendada)
python scripts/train_yolo.py `
    --tag baseline-v0 `
    --data data/raw/public/mango-v1-yolov8/data.yaml `
    --epochs 50

# Extraccion ya corre al final del training. Si quieres extraer manualmente:
python scripts/extract_yolo_artifacts.py `
    --run-dir ml/runs/detect/baseline-v0 `
    --tag baseline-v0
```

### EN-006 — Modelo final con dataset híbrido

```powershell
# Asumiendo que ya corriste el split (EN-003) y tienes data/processed/dataset.yaml
python scripts/train_yolo.py `
    --tag custom-v1 `
    --data data/processed/dataset.yaml `
    --epochs 100 `
    --resume-from ml/models/baseline-v0.pt
```

### RN-001 — Validar mAP@0.5 ≥ 0.85 en test set

```powershell
yolo val data=data/processed/dataset.yaml model=ml/models/custom-v1.pt split=test
# La salida muestra mAP50 por clase y agregado. Si >= 0.85 -> RN-001 cumplida.
```

### EN-007 — U-Net para severidad

Notebook separado en `notebooks/unet_severity.ipynb` (a crear cuando arranque). Entrena un U-Net sobre máscaras de las lesiones para estimar el porcentaje de área afectada.

### EN-008 — Artefactos de evaluación

Los gráficos copiados por `extract_yolo_artifacts.py` (results.png, PR_curve.png, confusion_matrix.png) son los artefactos de evaluación. Se referencian desde la evidencia de cada PBI.

### EN-009 — Export para producción

```powershell
yolo export model=ml/models/custom-v1.pt format=onnx imgsz=640
# Resultado: ml/models/custom-v1.onnx (consumible por ONNX Runtime en el backend)
```

## Recursos GPU

| Opción | Detalle |
|---|---|
| Local con GPU NVIDIA | Mejor performance. CUDA 11.8+ |
| Google Colab (free) | T4 GPU 12 h. Sube `dataset.yaml` + imágenes a Drive y monta. |
| Google Colab (Pro) | A100, sin límite de tiempo. |
| Kaggle Notebooks | T4 / P100. Acepta datasets pesados. |
| CPU | Solo para dry-run de smoke test, no para training real. |

## Scripts auxiliares

| Script | Propósito |
|---|---|
| [`scripts/train_yolo.py`](../scripts/train_yolo.py) | CLI para entrenar EN-005 y EN-006 |
| [`scripts/extract_yolo_artifacts.py`](../scripts/extract_yolo_artifacts.py) | Copia results.png, PR_curve.png, etc. y genera SUMMARY.md |
| [`scripts/split_dataset.py`](../scripts/split_dataset.py) | Genera el `dataset.yaml` que consume YOLO |
