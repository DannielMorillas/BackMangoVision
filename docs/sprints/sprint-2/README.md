# Sprint 2 — Construcción del Dataset

| Campo | Valor |
|---|---|
| Sprint | 2 de 5 |
| Duración planificada | 3 semanas (Semanas 4 a 6) |
| SP planificados | 39 |
| Sprint Goal | Tener un dataset híbrido (público + propio) de ≥ 768 imágenes anotadas y dividido en train/val/test, listo para entrenar modelos en Sprint 3. |

## PBIs del Sprint

| ID | Título | SP | Estado | Evidencia |
|---|---|---|---|---|
| EN-001 | Importar Dataset Público de Mango | 5 | 🟡 | [EN-001.md](evidencias/EN-001.md) — Opción E confirmada |
| EN-002 | Instalar y Configurar CVAT | 3 | 🟡 | [EN-002.md](evidencias/EN-002.md) — docs listos, falta ejecución |
| DO-001 | Documentar Protocolo de Captura de Campo | 3 | ✅ | [DO-001.md](evidencias/DO-001.md) |
| HU-009 | Realizar Sesiones de Captura en Casma | 8 | 🟡 | sesiones marzo–abril 2026 ejecutadas, falta copiar fotos |
| HU-010 | Anotar Imágenes con Bounding Boxes (CVAT → YOLO) | 13 | ⏳ | bloqueada por HU-009 y EN-002 |
| EN-003 | Dividir Dataset en Train / Val / Test (70/15/15) | 5 | 🟡 | [EN-003.md](evidencias/EN-003.md) — script listo |
| EN-004 | Crear y Validar dataset.yaml para YOLOv8 | 2 | 🟡 | [EN-004.md](evidencias/EN-004.md) — autogen ligada a EN-003 |

**Avance:** 1 ✅ + 5 🟡 + 1 ⏳ · scripts y docs completos · ejecución final espera fotos de Casma + anotación en CVAT.

### Apoyo adicional creado

- [`scripts/verify_yolo_dataset.py`](../../../scripts/verify_yolo_dataset.py) — validador de integridad YOLO (Bootstrap).
- [`scripts/select_for_annotation.py`](../../../scripts/select_for_annotation.py) — selecciona 120 imágenes balanceadas para anotar en CVAT (HU-010).
- [`scripts/split_dataset.py`](../../../scripts/split_dataset.py) — split estratificado + genera `dataset.yaml`.

## Plan de ejecución

```mermaid
gantt
    title Sprint 2 - flujo de tareas
    dateFormat  YYYY-MM-DD
    section Setup
    EN-002 CVAT      :done, en002, 2026-05-25, 2d
    EN-001 Importar publico :en001, 2026-05-25, 3d
    DO-001 Protocolo :do001, 2026-05-26, 2d
    section Campo
    HU-009 Captura Casma :hu009, after do001, 4d
    section Anotacion
    HU-010 Anotar CVAT :hu010, after hu009, 8d
    section Cierre
    EN-003 Split :en003, after hu010, 1d
    EN-004 dataset.yaml :en004, after en003, 1d
```

## Roles para Sprint 2

| Tarea | Responsable | Apoyo |
|---|---|---|
| EN-001 (importar público) | Patrick | Daniel valida con script |
| EN-002 (setup CVAT) | Daniel | — |
| DO-001 (protocolo) | Johan | Daniel revisa |
| HU-009 (captura Casma) | Patrick | Agrónomo ARA Export |
| HU-010 (anotación CVAT) | Patrick | Agrónomo valida 10% |
| EN-003 (split) | Daniel | Johan ejecuta script |
| EN-004 (dataset.yaml) | Daniel | — |

## Estructura de evidencias

Cada PBI cierra con un `evidencias/<ID>.md` con: resumen, archivos creados, comando de verificación, criterios, notas técnicas. Patrón idéntico al Sprint 1.

## Criterios de cierre del Sprint

- ✅ Dataset híbrido con ≥ 768 imágenes anotadas (≥ 150 por clase).
- ✅ Splits 70/15/15 generados con balance por clase preservado.
- ✅ `dataset.yaml` validado: `yolo train data=data/processed/dataset.yaml` no lanza errores de configuración.
- ✅ Validación cruzada del 10% por agrónomo de ARA Export documentada.
- ✅ Todas las evidencias en `docs/sprints/sprint-2/evidencias/`.
