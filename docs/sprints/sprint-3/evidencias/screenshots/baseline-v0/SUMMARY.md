# Resumen de run YOLO — `baseline-v0`

**Carpeta origen:** `ml\runs\baseline-v0`
**Fecha de extracción:** generada automáticamente por `scripts/extract_yolo_artifacts.py`

## Archivos copiados

- `results.png`
- `BoxPR_curve.png`
- `BoxF1_curve.png`
- `BoxP_curve.png`
- `BoxR_curve.png`
- `confusion_matrix.png`
- `confusion_matrix_normalized.png`
- `labels.jpg`
- `results.csv`
- `args.yaml`

## Métricas de la última época

| Métrica | Valor |
|---|---|
| `epoch` | 50 |
| `train/box_loss` | 0.34612 |
| `train/cls_loss` | 0.42803 |
| `train/dfl_loss` | 1.03889 |
| `val/box_loss` | 0.57936 |
| `val/cls_loss` | 0.70769 |
| `val/dfl_loss` | 1.24934 |
| `metrics/precision(B)` | 0.80939 |
| `metrics/recall(B)` | 0.86605 |
| `metrics/mAP50(B)` | 0.91292 |
| `metrics/mAP50-95(B)` | 0.80923 |
| `lr/pg0` | 4.96766e-05 |
| `time` | 1965.3 |
| `lr/pg1` | 4.96766e-05 |
| `lr/pg2` | 4.96766e-05 |

## Mejor época por `mAP@0.5` (epoch 44)

| Métrica | Valor |
|---|---|
| `epoch` | 44 |
| `time` | 1743.4 |
| `train/box_loss` | 0.38461 |
| `train/cls_loss` | 0.48153 |
| `train/dfl_loss` | 1.06965 |
| `metrics/precision(B)` | 0.88032 |
| `metrics/recall(B)` | 0.81144 |
| `metrics/mAP50(B)` | 0.91604 |
| `metrics/mAP50-95(B)` | 0.81036 |
| `val/box_loss` | 0.60446 |
| `val/cls_loss` | 0.75894 |
| `val/dfl_loss` | 1.28011 |
| `lr/pg0` | 0.000247716 |
| `lr/pg1` | 0.000247716 |
| `lr/pg2` | 0.000247716 |

## Cómo se cumple RN-001

RN-001 exige `mAP@0.5 ≥ 0.85` en el test set. La métrica `metrics/mAP50(B)` de la mejor época indica
el desempeño en el set de **validación** durante el training. Para la verificación final en el set de
**test**, ejecutar:

```powershell
yolo val data=data/processed/dataset.yaml model=ml/models/best.pt split=test
```

El número de `mAP50` reportado por ese comando es el que cuenta para cerrar RN-001.
