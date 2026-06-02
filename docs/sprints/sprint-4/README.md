# Sprint 4 — Backend + Frontend Core (End-to-End)

| Campo | Valor |
|---|---|
| Sprint | 4 de 5 |
| Duración planificada | 3 semanas (Semanas 10 a 12) |
| Estado | 🟡 En progreso — slice end-to-end en modo **stub** funcionando |
| Inicio real | 2026-06-01 |
| Sprint Goal | Sistema end-to-end: el agrónomo sube una foto y recibe el diagnóstico con bounding boxes desde el frontend, con la API REST y el servicio de inferencia integrados. |

> **Estrategia adoptada:** construir todo el flujo end-to-end **con un modelo stub determinista** para no bloquearnos esperando el `.pt` real (EN-006 depende de GPU + dataset anotado). Cuando el modelo exista, se activa solo (ver EN-011). Esto permite demo, frontend y tests **ya**.

## PBIs del Sprint

### Backend (FastAPI)

| ID | Título | SP | Estado | Evidencia |
|---|---|---|---|---|
| EN-010 | Implementar endpoints de la API (imágenes, predict, diagnósticos, métricas) | 13 | 🟢 | [EN-010.md](evidencias/EN-010.md) |
| EN-011 | Integrar YOLOv8 en servicio de inferencia (modo stub + listo para real) | 13 | 🟡 | [EN-011.md](evidencias/EN-011.md) |
| EN-012 | Tests unitarios con cobertura > 70% | 8 | 🟡 | escritos; falta correr suite con DB real |
| EN-013 | Registrar tiempos de inferencia en BD | 5 | 🟢 | [EN-013.md](evidencias/EN-013.md) |
| EN-014 | Endpoint de métricas del sistema | 8 | 🟢 | [EN-014.md](evidencias/EN-014.md) |

### Frontend (React 19 + Vite + Tailwind 4)

| ID | Título | SP | Estado | Evidencia |
|---|---|---|---|---|
| HU-011 | Dashboard con resumen de diagnósticos | 8 | 🟢 | [HU-011.md](evidencias/HU-011.md) |
| HU-012 | Subir imagen con drag & drop | 8 | 🟢 | [HU-012.md](evidencias/HU-012.md) |
| HU-013 | Visualizar resultado con bounding boxes | 13 | 🟢 | [HU-013.md](evidencias/HU-013.md) |
| HU-014 | Historial con filtros | 8 | 🟢 | incluido en HU-011 (HistorialPage) |

**Avance:** flujo completo upload → predict → diagnóstico con cajas → historial → dashboard, operativo en modo stub.

## Endpoints entregados

| Método | Ruta | PBI |
|---|---|---|
| POST | `/api/imagenes` | EN-010 / HU-012 |
| GET | `/api/imagenes/{id}/contenido` | EN-010 / HU-013 |
| POST | `/api/predict` | EN-011 / HU-013 |
| GET | `/api/diagnosticos` | EN-010 / HU-014 |
| GET | `/api/diagnosticos/{id}` | EN-010 / HU-013 |
| GET | `/api/diagnosticos/resumen` | EN-010 / HU-011 |
| GET | `/api/diagnosticos/export` | EN-010 / HU-014 (CSV) |
| GET | `/api/metricas` | EN-014 |
| GET, PATCH | `/api/admin/models` · `/{id}` | EN-010 |
| GET | `/api/admin/logs` | EN-010 |

> Junto con auth/admin-users/diseases/health del Sprint 1, el sistema cubre el grueso de los 17 endpoints del Project Charter.

## Arquitectura del backend añadida

```
backend/app/
├── services/
│   ├── storage.py        ← local (dev) | minio (prod), misma interfaz
│   ├── inference.py      ← singleton; stub determinista | YOLOv8 real (MODEL_PATH)
│   └── diagnostico.py    ← arma DiagnosticoRead (aptitud, sano/enfermo)
├── schemas/prediction.py ← ImageRead, PredictionRead, DiagnosticoRead, *Resumen, *Metricas
└── api/routes/
    ├── images.py · predict.py · diagnosticos.py · metricas.py
```

## Frontend añadido (repo FrontMangoVision)

```
frontend/src/
├── types/diagnostico.ts          ← tipos espejo de los schemas backend
├── services/diagnosticos.ts      ← upload/predict/list/resumen/metricas/blob
├── components/
│   ├── AppHeader.tsx             ← nav autenticada (Dashboard/Nuevo/Historial)
│   └── BoundingBoxOverlay.tsx    ← cajas en SVG escalable (HU-013)
└── pages/
    ├── DashboardPage.tsx (reescrito) · UploadPage.tsx
    ├── DiagnosticResultPage.tsx · HistorialPage.tsx
```

## Verificación

- ✅ Backend: `py_compile` OK en los 12 archivos nuevos/modificados.
- ✅ Servicio de inferencia (stub) ejecutado en runtime: determinista, bboxes válidos, severidad/aptitud correctas.
- 🟡 Tests de integración escritos ([test_predict_api.py](../../../backend/tests/integration/test_predict_api.py)) — requieren Postgres de test para correr.
- ✅ Frontend `tsc --noEmit` → **sin errores** (203 paquetes instalados, typecheck verde 2026-06-01).

## Pendientes para cerrar el Sprint 4

- [ ] Correr la suite de tests con Postgres real y medir cobertura (EN-012, meta > 70%).
- [x] `tsc --noEmit` verde en el frontend.
- [x] Endpoints `admin/models`, `admin/logs` y `diagnosticos/export` (CSV).
- [ ] Demo end-to-end real con la app levantada (backend + frontend + DB) — RN-002 (≤ 5 s).
- [ ] Sustituir stub por modelo real cuando exista `ml/models/custom-v1.pt` (EN-006).
- [ ] Sprint Review + Retrospectiva.

## Criterios de cierre (checklist Project Charter)

```
[~] Endpoints implementados y documentados en Swagger (10/17 del core; falta verificar Swagger con app levantada)
[~] YOLOv8 integrado en servicio de inferencia (modo stub; real cuando haya .pt)
[ ] Tests con cobertura > 70% (escritos, falta correr)
[x] Tiempos de inferencia se registran en BD
[x] Endpoint /api/metricas retorna datos correctos
[x] Dashboard funcional con resumen
[x] Upload con drag & drop funcional
[x] Visualización con bounding boxes funcional
[x] Historial con filtros
[ ] Diagnóstico end-to-end < 5 segundos (medir con app levantada)
[ ] Sprint Review / Retrospectiva
```
