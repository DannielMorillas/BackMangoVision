# Sprint 1 — Acceso al Sistema + Infraestructura

| Campo | Valor |
|---|---|
| Sprint | 1 de 5 |
| Duración planificada | 3 semanas |
| SP planificados | 46 |
| Sprint Goal | Que un ingeniero agrónomo de ARA Export pueda acceder al sistema con credenciales seguras y que la infraestructura técnica esté lista para construir el resto del producto. |

## Estado de PBIs

| ID | Título | SP | Estado | Evidencia |
|---|---|---|---|---|
| EN-000 | Crear Repositorio Git con Estructura Completa | 3 | ✅ | [evidencias/EN-000.md](evidencias/EN-000.md) |
| EN-017 | Instalar Docker, Python 3.11 y Node.js 20 | 2 | ✅ | [evidencias/EN-017.md](evidencias/EN-017.md) |
| EN-018 | Levantar PostgreSQL y MinIO con Docker | 3 | ✅ | [evidencias/EN-018.md](evidencias/EN-018.md) |
| EN-019 | Configurar Archivo .env con Variables de Entorno | 2 | ✅ | [evidencias/EN-019.md](evidencias/EN-019.md) |
| EN-020 | Ejecutar Primera Migración Alembic | 3 | ✅ | [evidencias/EN-020.md](evidencias/EN-020.md) |
| EN-021 | Insertar Catálogo de Enfermedades | 2 | ✅ | [evidencias/EN-021.md](evidencias/EN-021.md) |
| HU-001 | Ver Landing Page Informativa | 5 | ✅ | [evidencias/HU-001.md](evidencias/HU-001.md) |
| HU-002 | Ver Sección de Enfermedades en Landing | 3 | ✅ | [evidencias/HU-002.md](evidencias/HU-002.md) |
| HU-003 | Acceder al Sistema desde Landing | 2 | ✅ | [evidencias/HU-003.md](evidencias/HU-003.md) |
| HU-004 | Iniciar Sesión con Email y Contraseña | 5 | ✅ | [evidencias/HU-004.md](evidencias/HU-004.md) |
| HU-005 | Cerrar Sesión del Sistema | 3 | ✅ | [evidencias/HU-005.md](evidencias/HU-005.md) |
| HU-006 | Recuperar Contraseña Olvidada | 5 | ✅ | [evidencias/HU-006.md](evidencias/HU-006.md) |
| HU-007 | Crear Cuenta de Ingeniero Agrónomo | 5 | ✅ | [evidencias/HU-007.md](evidencias/HU-007.md) |
| HU-008 | Desactivar o Reactivar Cuenta de Usuario | 3 | ✅ | [evidencias/HU-008.md](evidencias/HU-008.md) |

**Avance:** 14/14 PBIs · 46/46 SP · **Sprint 1 cerrado** ✅

## Resumen de tests

| Capa | Framework | Tests | Estado |
|---|---|---|---|
| Backend | Pytest | 41 (+1 skipped) | ✅ |
| Frontend | Vitest | 18 | ✅ |
| **Total** | — | **59** | **✅** |

## Incidencias resueltas

Ver [incidencias.md](incidencias.md) — 6 incidencias documentadas con diagnóstico y resolución (puerto Postgres / WSL, UTF-8 cp1252, Alembic env.py, dominio `.test` rechazado, certificado SSL en npm, harness file-tracking).

## Sprint Review — Acta

- **Fecha de cierre:** 2026-05-23
- **PBIs aceptados:** 14 / 14 (100 %)
- **SP completados:** 46 / 46 (100 %)
- **Velocity reportada:** 46 SP
- **Demostración:** Landing pública en `/`, login funcional, dashboard protegido, recuperación de contraseña con stub local, gestión de usuarios para admin, catálogo de enfermedades dinámico desde backend.
- **Hitos cumplidos:** M1 — Acceso operativo (landing + login + cuentas creadas + BD inicializada).

## Cómo levantar el sistema end-to-end

```powershell
# 1. Servicios
cd c:\Users\Patrick Isla\Desktop\notion\MangoVision
docker compose up -d

# 2. Backend
cd backend
$env:PYTHONPATH = "."
.\.venv\Scripts\python.exe -m alembic upgrade head
# Aplicar seed enfermedades (una vez):
docker cp ..\db\seeds\diseases.sql mangovision-postgres:/tmp/diseases.sql
docker exec mangovision-postgres psql -U mangovision -d mangovision -f /tmp/diseases.sql
# Crear admin inicial (una vez):
.\.venv\Scripts\python.exe scripts/seed_initial_admin.py
# Levantar API:
.\.venv\Scripts\uvicorn.exe app.main:app --reload --port 8000

# 3. Frontend (otra terminal)
cd c:\Users\Patrick Isla\Desktop\notion\MangoVision\frontend
$env:NODE_OPTIONS = "--use-system-ca"
npm run dev
# Abrir http://localhost:5173

# Credenciales: admin@araexport.example / CambiameYa#2026
```

## Definition of Done aplicado

Cada PBI se considera cerrado cuando:

1. Código mergeado a `develop`.
2. Tests unitarios verdes (Pytest o Vitest según capa).
3. Criterios de aceptación marcados con evidencia (comando ejecutado, screenshot, o test que demuestra el criterio).
4. Documento `evidencias/<ID>.md` creado con: resumen, archivos tocados, cómo probar, screenshots/output.

## Convención de evidencia

Archivo `evidencias/<ID>.md` con secciones:

- **Resumen** — qué hace el PBI en una frase.
- **Archivos** — lista de archivos creados/modificados.
- **Cómo probar** — comandos exactos para reproducir.
- **Criterios verificados** — checklist con ✅ y referencia al test o screenshot.
- **Notas técnicas** — decisiones, deudas o desvíos del plan.
