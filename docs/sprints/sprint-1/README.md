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
| HU-004 | Iniciar Sesión con Email y Contraseña | 5 | ⏳ | — |
| HU-005 | Cerrar Sesión del Sistema | 3 | ⏳ | — |
| HU-006 | Recuperar Contraseña Olvidada | 5 | ⏳ | — |
| HU-007 | Crear Cuenta de Ingeniero Agrónomo | 5 | ⏳ | — |
| HU-008 | Desactivar o Reactivar Cuenta de Usuario | 3 | ⏳ | — |

**Avance:** 9/14 PBIs · 25/46 SP

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
