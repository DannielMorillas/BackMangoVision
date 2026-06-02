# Sprint 4 — Retrospectiva

| Campo | Valor |
|---|---|
| Sprint | 4 de 5 |
| Fecha sugerida | Último viernes Semana 12 (tras el Review) |
| Facilita | Johan Juares (Scrum Master) |
| Formato | Start / Stop / Continue |
| Estado | 📋 Borrador con observaciones reales del desarrollo; el equipo lo completa/ajusta en la ceremonia |

---

## Datos del Sprint

- **SP planificados:** 76 (recomendado, sin sobrecarga)
- **SP construidos:** ~76 (código completo back + front)
- **SP aceptados:** a definir en el Review (gran parte condicional a la demo en vivo)
- **Sprint Goal:** 🟡 cumplido a nivel build; pendiente validación end-to-end
- **Tiempo de diagnóstico end-to-end:** ⏳ por medir
- **Cobertura de tests:** ⏳ por medir (tests escritos, falta correrlos con DB)

---

## Start / Stop / Continue

### ➕ Start (empezar a hacer)
- **Levantar la base de datos e integrar temprano.** Construimos todo el slice (back + front) sin correrlo junto; el riesgo de integración quedó concentrado al final. Integrar desde la primera semana del sprint.
- **CI mínimo** que corra `pytest` (backend) y `tsc --noEmit` (frontend) en cada push, para no depender de verificación manual.
- **Commitear seguido.** Se acumuló mucho trabajo sin versionar; conviene commits más chicos y frecuentes.

### ➖ Stop (dejar de hacer)
- **Acumular cambios sin commitear.** Un solo lote gigante dificulta la trazabilidad y el reparto por PBI.
- **Posponer la prueba end-to-end** hasta tener "todo listo": valida supuestos demasiado tarde.

### 🔁 Continue (seguir haciendo)
- **Enfoque "stub-first":** el modelo stub determinista permitió construir y demostrar todo el sistema sin esperar la GPU/dataset. Excelente para no bloquearnos.
- **Documentar cada PBI con su evidencia** en `docs/sprints/` — mantiene el repo auditable.
- **Componentes reutilizables** en el frontend (AppHeader, overlay SVG) y servicios desacoplados en el backend (storage/inference conmutables).

---

## Acciones acordadas para Sprint 5 (FINAL)

| # | Acción | Responsable | Fecha límite |
|---|---|---|---|
| 1 | Levantar app completa (Docker+Postgres+seed) y correr suite de tests → medir cobertura | Patrick | Inicio Sprint 5 |
| 2 | Demo end-to-end + benchmark RN-002 (≤ 5 s) y registrar resultado | Patrick + Johan | Semana 13 |
| 3 | Entrenar modelo real (EN-006) en Colab/Kaggle y reemplazar el stub (`MODEL_PATH`) | Patrick | Semana 13 |
| 4 | Configurar CI (pytest + tsc) en GitHub Actions | Daniel | Semana 13 |
| 5 | Commitear lockfiles para builds reproducibles del equipo | Equipo | Continuo |

---

## Indicadores de salud del proceso (Sprint 4)

| Indicador | Meta | Sprint 4 |
|---|---|---|
| % Cumplimiento Sprint Goal | 100 % | 🟡 build 100% / demo pendiente |
| Velocity | ≥ 40 SP | ~76 SP construidos |
| Cobertura de tests | > 70 % | ⏳ por medir |
| Bugs post-sprint | < 3 | ⏳ por medir en demo |
