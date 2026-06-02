# Sprint 4 — Sprint Review

| Campo | Valor |
|---|---|
| Sprint | 4 de 5 — Backend + Frontend Core (End-to-End) |
| Fecha sugerida | Último viernes Semana 12 |
| Asistentes | Patrick Isla (PO/Dev), Daniel Morillas (PM), Johan Juares (SM), Walter Cueva (Asesor) + agrónomo ARA Export |
| Estado del documento | 📋 Preparado con el build actual — la **aceptación final** queda sujeta a la demo en vivo + corrida de tests |

> **Nota de honestidad:** este guion se preparó sobre el código ya construido y versionado. Lo que **no** está validado todavía: la demo end-to-end con la app levantada (DB + back + front), la cobertura real de tests y el modelo real. Esos puntos se marcan como ⏳ y condicionan la aceptación.

---

## 1. Sprint Goal — ¿se cumplió?

> *"Sistema end-to-end: el agrónomo sube una foto y recibe el diagnóstico con bounding boxes desde el frontend, con la API REST y el servicio de inferencia integrados."*

**Estado: 🟡 Cumplido a nivel de construcción, pendiente de demo en vivo.**
Todo el flujo está implementado y verificado de forma aislada (typecheck, `py_compile`, stub en runtime). Falta ejecutarlo integrado para aceptarlo formalmente.

---

## 2. Incremento entregado

### Backend (FastAPI) — repo BackMangoVision
- 10 endpoints del core operativos (imágenes, predict, diagnósticos +resumen +export CSV, métricas, admin/models, admin/logs).
- Servicio de inferencia con **modo stub determinista** + camino a YOLOv8 real sin tocar la API.
- Storage local/MinIO conmutable; tiempos de inferencia persistidos.

### Frontend (React 19 + Vite + Tailwind) — repo FrontMangoVision
- Dashboard con resumen, Upload drag & drop, Resultado con bounding boxes (SVG), Historial filtrable con paginación.
- `tsc --noEmit` en verde.

---

## 3. PBIs a presentar y aceptar

| ID | Título | SP | Estado build | Aceptación |
|---|---|---|---|---|
| EN-010 | Endpoints de la API | 13 | 🟢 10/17 del core | Condicional a demo Swagger |
| EN-011 | Integrar YOLOv8 (inferencia) | 13 | 🟡 stub listo | Parcial (real depende de EN-006) |
| EN-012 | Tests cobertura >70% | 8 | 🟡 escritos | ⏳ falta correr con DB |
| EN-013 | Tiempos de inferencia en BD | 5 | 🟢 | Aceptable |
| EN-014 | Endpoint de métricas | 8 | 🟢 | Aceptable |
| HU-011 | Dashboard | 8 | 🟢 | Condicional a demo |
| HU-012 | Upload drag & drop | 8 | 🟢 | Condicional a demo |
| HU-013 | Resultado con bounding boxes | 13 | 🟢 | Condicional a demo |
| HU-014 | Historial con filtros | 8 | 🟢 | Condicional a demo |

**SP construidos:** ~76 (sobre 76 planificados, recomendado). **SP aceptables hoy sin demo:** EN-013 + EN-014 (13 SP). El resto se acepta tras la demo en vivo.

---

## 4. Guion de la demostración (end-to-end)

> Requisito previo: app levantada. Ver [runbook de puesta en marcha](#) (a generar) o pasos del README del backend.

1. **Login** como agrónomo → entra al **Dashboard** (muestra KPIs y barras por enfermedad).
2. Clic en **"Nuevo diagnóstico"** → arrastrar una foto de mango (drag & drop) → completar lote/parcela → **"Analizar imagen"**.
3. El sistema sube la imagen, ejecuta inferencia y redirige al **resultado**: imagen con **bounding boxes** dibujados, panel con aptitud (apto/no_apto), severidad, % de área y tiempo de inferencia.
   - Señalar el badge **"provisional"** (modo stub) — se quitará al integrar el modelo real.
4. Ir al **Historial** → filtrar por enfermedad / lote / aptitud → abrir un diagnóstico → **Exportar CSV**.
5. (Admin) Mostrar **gestión de modelos** (`admin/models`) y **logs de actividad** (`admin/logs`).
6. Medir el **tiempo end-to-end** (objetivo RN-002 ≤ 5 s) — registrar el valor real.

---

## 5. Lo que NO se demuestra este sprint (transparencia con el cliente)

- El **diagnóstico real** (el stub da resultados plausibles pero no reales) — depende del modelo entrenado (EN-006, Sprint 3, bloqueado por GPU + dataset anotado).
- Validación con usuarios reales y experimento → Sprint 5.

---

## 6. Feedback recogido (a completar en la reunión)

| # | Comentario | Origen | Acción |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

---

## 7. Decisión de aceptación

- [ ] PBIs aceptados: ___________
- [ ] PBIs rechazados / con observaciones: ___________
- [ ] Tiempo end-to-end medido: ___ s
- [ ] Cobertura de tests medida: ___ %
