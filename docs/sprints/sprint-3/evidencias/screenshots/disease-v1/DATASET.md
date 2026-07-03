# Dataset de detección de enfermedades — `disease-v1`

Evidencia de **preparación y verificación** del dataset usado para el baseline público de detección de enfermedades (fase intermedia de EN-006). Generada el 2026-07-03.

## Procedencia

| Campo | Valor |
|---|---|
| Nombre | Mango Leaf detection (v2) |
| Fuente | Roboflow Universe — workspace `penpixel`, proyecto `mango-leaf-detection-7abk6` |
| URL | https://universe.roboflow.com/penpixel/mango-leaf-detection-7abk6/dataset/2 |
| Licencia | CC BY 4.0 |
| Formato | YOLOv8 (detección, bounding boxes) |
| Ubicación en repo | `data/raw/public/mango-leaf-disease-yolov8/` |

## Clases (`nc: 8`)

`['Anthracnose', 'Bacterial-Canker', 'Cutting-Weevil', 'Die-Back', 'Gall-Midge', 'Healthy', 'Powdery-Mildew', 'Sooty-Mould']`

**Mapeo al catálogo MangoVision:** `Anthracnose` → antracnosis y `Powdery-Mildew` → oídio coinciden con el catálogo objetivo. `Healthy` ≈ sano. Las demás (Bacterial-Canker, Cutting-Weevil, Die-Back, Gall-Midge, Sooty-Mould) son enfermedades/plagas de hoja fuera del catálogo — se conservan como clases del detector público, pero no forman parte del alcance del modelo final EN-006.

## Verificación de integridad

| Split | Imágenes | Labels | Bounding boxes |
|---|---|---|---|
| train | 2000 | 2000 | 1988 |
| valid | 191 | 191 | 190 |
| test | 95 | 95 | 93 |
| **Total** | **2286** | **2286** | **2271** |

- ✅ Cada imagen tiene su label (`0` imágenes sin `.txt`).
- ✅ `0` labels huérfanos.
- ✅ `0` problemas de formato; todos los `class_id` en rango `[0..7]`; coordenadas normalizadas en `[0..1]`.
- ℹ️ 15 labels vacíos (imágenes de fondo / negativas) — comportamiento válido en YOLO, aportan ejemplos sin lesión.

## Distribución de bounding boxes por clase

| Clase | train | valid | test | TOTAL |
|---|---|---|---|---|
| Anthracnose | 297 | 28 | 13 | 338 |
| Bacterial-Canker | 291 | 28 | 14 | 333 |
| Cutting-Weevil | 192 | 19 | 9 | 220 |
| Die-Back | 227 | 22 | 10 | 259 |
| Gall-Midge | 252 | 25 | 12 | 289 |
| Healthy | 189 | 17 | 9 | 215 |
| Powdery-Mildew | 276 | 26 | 13 | 315 |
| Sooty-Mould | 264 | 25 | 13 | 302 |

Dataset balanceado (ratio máx/mín ≈ 1.6) y con las 8 clases presentes en los tres splits — no hay clases con 0 muestras en validación ni en test.

## Limitación (relevante para la tesis)

Es un dataset de **hoja**, no de **fruto Kent**. Sirve para entrenar y validar el pipeline de detección de enfermedades y para el experimento de transfer learning (O1 vs O2), pero **no reemplaza** al dataset propio de ARA Export (fotos de Casma, 5 clases del catálogo, aún pendiente de anotación en CVAT — ver EN-006 y HU-009). El baseline de enfermedades sobre datos públicos de-riesga EN-006 mientras llega el dataset de fructificación.
