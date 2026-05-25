# Dataset: mango-v1-yolov8

| Campo | Valor |
|---|---|
| Fuente | Roboflow Universe |
| URL | https://universe.roboflow.com/daniel-morillas/mango-0igyk-xk6in/dataset/1 |
| Workspace | daniel-morillas |
| Proyecto | mango-0igyk-xk6in |
| Versión | v1 (2025-12-10) |
| Licencia | CC BY 4.0 |
| Formato | YOLOv8 (imágenes + .txt YOLO) |
| Pre-processing | Ninguno aplicado |

## Inventario

| Split | Imágenes | Labels (.txt) |
|---|---|---|
| train | 2041 | 2041 |
| valid | 583 | 583 |
| test | 292 | 292 |
| **Total** | **2916** | **2916** |

## Distribución de bounding boxes por clase

| ID YOLO | Clase original | Bboxes | % |
|---|---|---|---|
| 0 | `ripe` (maduro) | 750 | 29.4% |
| 1 | `un_ripe` (inmaduro) | 1805 | 70.6% |
| | **Total** | **2555** | **100%** |

## ⚠️ Incompatibilidad con el catálogo MangoVision

Este dataset **NO contiene clases de enfermedades**. Sus dos clases son sobre **estado de maduración** del fruto:

| Clase Roboflow | Clase MangoVision | Mapeo |
|---|---|---|
| `ripe` | — | ❌ Sin equivalente directo |
| `un_ripe` | — | ❌ Sin equivalente directo |

### Cómo se aprovecha igual

Aunque las clases no coinciden, el dataset es útil para:

1. **Pre-training de localización de frutos:** los bboxes ya enseñan al modelo a *encontrar mangos* en una imagen. Eso es un building block antes de clasificar enfermedades sobre el fruto detectado.
2. **Transfer learning:** usar los pesos resultantes como punto de partida para el modelo de enfermedades (entrenado sobre el dataset propio + mango-leaf-disease-cls).
3. **Validación de detección:** si el modelo final detecta correctamente los frutos del test set de Roboflow, sabemos que la parte de localización funciona.

## Cómo se descargó

Exportado vía la UI de Roboflow el 10 de diciembre de 2025 por el workspace `daniel-morillas`. Descomprimido en `c:\...\BackMangoVision\data\raw\public\mango-v1-yolov8\` el 24 de mayo de 2026.

## Estructura

```
mango-v1-yolov8/
├── README.dataset.txt
├── README.roboflow.txt
├── data.yaml                 ← config original Roboflow (NO usar para entrenamiento final)
├── train/
│   ├── images/ (2041 jpg)
│   └── labels/ (2041 txt)
├── valid/
│   ├── images/ (583 jpg)
│   └── labels/ (583 txt)
└── test/
    ├── images/ (292 jpg)
    └── labels/ (292 txt)
```
