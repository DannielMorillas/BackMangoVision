# Bootstrap Sprint 2 — Estructura de datos y herramientas auxiliares

| Campo | Valor |
|---|---|
| Tipo | Infraestructura del sprint (preámbulo a EN-001) |
| Sprint | 2 |
| Estado | ✅ Done |
| Fecha | 2026-05-24 |
| Responsable | Daniel Morillas |

---

## Resumen

Antes de arrancar formalmente con EN-001 (importar el dataset público que el equipo ya tenía en otra PC), se preparó la **infraestructura de carpetas y utilidades** necesarias para los 7 PBIs del Sprint 2. Esta evidencia cubre el trabajo "previo" que no encaja en un único PBI pero es prerrequisito de todos.

## Entregables

### 1. Estructura de `data/`

Carpeta nueva en la raíz de `BackMangoVision`, con sub-estructura completa lista para recibir datos:

```
data/
├── README.md                        ← convencion y mapeo de clases (versionado)
├── raw/
│   ├── public/{images,labels}/      ← gitignored — dataset publico Kaggle/Roboflow
│   └── aragroexport/{images,labels} ← gitignored — capturas propias de Casma
├── interim/                         ← gitignored — limpieza y conversiones
└── processed/
    ├── train/{images,labels}/       ← gitignored — split final
    ├── val/{images,labels}/         ← gitignored
    └── test/{images,labels}/        ← gitignored
```

[`data/README.md`](../../../../data/README.md) documenta:
- Convención de carpetas.
- Mapeo de las 5 clases del catálogo al orden YOLO (id 0 = sano, ..., id 4 = otras_lesiones).
- Pasos para integrar dataset público que el equipo trae de otra PC.
- Pasos para recibir capturas propias después de HU-009.

### 2. `.gitignore` actualizado

Antes el `.gitignore` tenía caracteres UTF-16 huérfanos al final (de un append PowerShell `>>` previo) y mezclaba reglas de frontend con backend. Reescrito limpio con secciones:

- Python (venv, pycache, pytest, coverage)
- Entorno (.env)
- IDEs
- Docker (postgres-data, minio-data, cvat-data)
- ML (modelos `*.pt`, `*.onnx`, weights)
- **Datasets** (`data/raw/`, `data/interim/`, `data/processed/`)
- Logs

Resultado: ningún byte de dataset se sube por accidente a GitHub. Solo `data/README.md` (~3 KB) viaja en el repo.

### 3. Script `scripts/verify_yolo_dataset.py`

Utilidad standalone para validar un dataset YOLO antes de procesarlo. Detecta:

- Imágenes sin label o labels huérfanos.
- IDs de clase fuera del rango [0..4].
- Coordenadas YOLO mal normalizadas (fuera de [0..1]).
- Distribución de bounding boxes por clase (gráfico ASCII).

Uso:

```powershell
cd c:\Users\Patrick Isla\Desktop\notion\BackMangoVision
python scripts\verify_yolo_dataset.py data\raw\public
python scripts\verify_yolo_dataset.py data\raw\aragroexport
```

Exit code 0 si está OK, 1 si encuentra inconsistencias. Útil tanto al integrar el dataset público (EN-001) como al cerrar la anotación propia (HU-010).

### 4. Setup de CVAT documentado

[`cvat/README.md`](../../../../cvat/README.md) con instrucciones para clonar el repo oficial de CVAT v2.18 y levantarlo en una carpeta paralela. Mapeo de clases CVAT → YOLO documentado para que el orden de creación de labels sea exacto.

Detalle en [EN-002.md](EN-002.md).

### 5. Sprint 2 README + DO-001 borrador

- [`docs/sprints/sprint-2/README.md`](../README.md) — plan con los 7 PBIs, responsables y gantt.
- [`docs/sprints/sprint-2/evidencias/DO-001.md`](DO-001.md) — protocolo de captura en Casma (borrador, fechas pendientes).

## Cómo probar

```powershell
cd c:\Users\Patrick Isla\Desktop\notion\BackMangoVision

# 1. Estructura data/ existe
Get-ChildItem data -Recurse -Directory | Select-Object -ExpandProperty FullName

# 2. .gitignore ignora data/raw/
git check-ignore data/raw/public/images/foo.jpg
# → debe devolver la ruta (ignorada)

# 3. verify_yolo_dataset.py corre sin error sintáctico
python -c "import ast; ast.parse(open('scripts/verify_yolo_dataset.py').read()); print('OK syntax')"
```

## Criterios verificados

- [x] Estructura `data/` con 11 sub-carpetas creadas.
- [x] `data/README.md` documenta convención y mapeo de clases.
- [x] `.gitignore` excluye `data/raw/`, `data/interim/`, `data/processed/`.
- [x] `scripts/verify_yolo_dataset.py` parseable y ejecutable con `--help`.
- [x] `cvat/README.md` documenta instalación, workflow y export YOLO.
- [x] `docs/sprints/sprint-2/README.md` listo con 7 PBIs y responsables.
- [x] DO-001 borrador esperando fechas de Casma.

## Próximo paso del sprint

Cuando Patrick copie el dataset YOLO desde su otra PC a `data/raw/public/`, ejecutará:

```powershell
python scripts\verify_yolo_dataset.py data\raw\public
```

El output define si EN-001 puede cerrarse directo o si necesita remap de IDs de clase.
