# Sprint 1 — Incidencias y pruebas que fallaron durante el desarrollo

Este documento registra los problemas que aparecieron durante la construcción del Sprint 1, cómo se diagnosticaron y cómo quedaron resueltos. Sirve como referencia para futuros sprints y para que el equipo no tropiece dos veces con la misma piedra.

---

## I-01 · Puerto 5432 ocupado por WSL al levantar Postgres

| Campo | Valor |
|---|---|
| Cuándo | Levantando `docker compose up -d` (EN-018) |
| Síntoma | `Bind for 0.0.0.0:5432 failed: port is already allocated` |
| Diagnóstico | `Get-NetTCPConnection -LocalPort 5432` mostró `wslrelay (PID 23248)` ocupando el puerto. |
| Causa | El usuario tiene un PostgreSQL en WSL (probablemente de otro proyecto) cuyo socket se publica vía `wslrelay` en el host. |
| Resolución inicial | Cambiar el mapeo del contenedor a `5433:5432`. |
| Recaída | En `5433` también había un postgres fantasma (mismo origen WSL), pero Python conectaba a un *otro* postgres allí que tenía credenciales distintas → `auth failed`. |
| Resolución final | Mover el contenedor a `55432:5432` (puerto improbable). Actualizar `DATABASE_URL`. |
| Tests asociados | `test_database_connection`, `test_all_seven_tables_exist` |
| Archivos | [docker-compose.yml](../../../docker-compose.yml), [.env.example](../../../.env.example) |

---

## I-02 · UTF-8 corrompido al aplicar `db/seeds/diseases.sql` en Windows

| Campo | Valor |
|---|---|
| Cuándo | Tras `EN-021` (carga inicial del catálogo). |
| Síntoma | `assert name == "Oídio"  →  'O??dio' == 'Oídio'` falla. |
| Diagnóstico | El nombre en la BD quedó como `O??dio` porque PowerShell `Get-Content` lee con cp1252 antes de pipe a `docker exec -i psql`, y reemplaza los caracteres no representables por `?`. |
| Causa | Encoding default de `Get-Content` en Windows PowerShell 5.1 es cp1252, no UTF-8. |
| Resolución | Usar `docker cp` + `psql -f`: el archivo viaja como bytes UTF-8 puros al contenedor y se aplica desde adentro. |
| Documentado en | [db/seeds/README.md](../../../db/seeds/README.md) |
| Tests asociados | `test_unicode_preserved_in_disease_names`, `test_unicode_oidio_returned_correctly` |

---

## I-03 · Alembic conectaba al postgres equivocado (env.py incompleto)

| Campo | Valor |
|---|---|
| Cuándo | Primera ejecución de `alembic revision --autogenerate` (EN-020). |
| Síntoma | `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:driver` |
| Diagnóstico | El `env.py` autogenerado por `alembic init` usa la URL declarativa de `alembic.ini`, que tiene un placeholder `driver://...`. |
| Causa | Faltaba inyectar `Settings.database_url` en `config.set_main_option("sqlalchemy.url", ...)` ANTES del `engine_from_config`. |
| Resolución | Reescribir `alembic/env.py` para cargar `get_settings()` e importar `app.models` (registra todas las tablas en `Base.metadata`). |
| Archivo | [backend/alembic/env.py](../../../backend/alembic/env.py) |

---

## I-04 · `EmailStr` rechazó el dominio `.test` (TLD reservado)

| Campo | Valor |
|---|---|
| Cuándo | Primera ejecución de los 18 tests de auth (HU-004 a HU-008). |
| Síntoma | `422 Unprocessable Entity` en `POST /api/auth/login` con mensaje: *"The part after the @-sign is a special-use or reserved name that cannot be used with email."* |
| Diagnóstico | `email-validator` (la librería que respalda a `pydantic.EmailStr`) sigue RFC 2606 y rechaza TLDs reservados como `.test`, `.example`, `.invalid`. |
| Causa | Convención clásica de tests `usuario@empresa.test` no es válida con validador estricto. |
| Resolución | Reemplazar todos los emails de tests por `@example.com` (un dominio reservado *que sí* está en la allow-list de email-validator). |
| Comando | `sed -i 's/@araexport\.test/@example.com/g' tests/integration/test_auth.py tests/conftest.py` |
| Tests afectados | Las 18 pruebas del archivo `test_auth.py` pasaron a verdes inmediatamente tras el cambio. |

---

## I-05 · `npm install` falla con `UNABLE_TO_VERIFY_LEAF_SIGNATURE`

| Campo | Valor |
|---|---|
| Cuándo | Primer `npm install` del frontend (HU-001). |
| Síntoma | `npm error code UNABLE_TO_VERIFY_LEAF_SIGNATURE` · `unable to verify the first certificate`. |
| Diagnóstico | Algún componente del host (antivirus, proxy corporativo o software de inspección TLS) intercepta el handshake con `registry.npmjs.org` y presenta un certificado firmado por una CA que Node no conoce. |
| Resolución | `NODE_OPTIONS=--use-system-ca` antes de `npm install`. Esto hace que Node lea el almacén de certificados de Windows (donde la CA del software interceptor sí está confiada). |
| Efecto secundario | El install completó en ~4 horas (vs ~1 minuto normal). La interceptación TLS añade latencia a cada request. Aceptable para desarrollo, pero relevante para CI/CD en futuro. |
| Persistencia | Para sesiones futuras: `setx NODE_OPTIONS "--use-system-ca"` (Windows permanente). |
| Archivo | Documentado aquí; no afecta código del proyecto. |

---

## I-06 · `Write` falló por "File has not been read yet" en archivo recién creado por proceso externo

| Campo | Valor |
|---|---|
| Cuándo | Tras `alembic init` que creó `alembic/env.py`. |
| Síntoma | `Write` y `Edit` rechazaron sobrescribir `env.py` con "File has not been read yet". |
| Causa | El harness rastrea qué archivos he leído. Los archivos creados por procesos externos (no por mí vía `Write`) deben pasar por `Read` antes de modificarlos. |
| Resolución | Hacer `Read` del archivo con `limit=10` (solo para registrarlo en el harness) y luego `Write`. |
| Aprendizaje | Cuando un comando genera archivos en disco, hago `Read` antes de editarlos. |

---

## Resumen de tests "negativos" (que verifican que el sistema falle bien)

Estos no son fallos del desarrollo, son tests que **esperan** un error para asegurar el comportamiento defensivo. Se listan aquí como referencia:

| Test | HU | Verifica que el sistema rechace |
|---|---|---|
| `test_login_wrong_password_returns_401` | HU-004 | Login con contraseña incorrecta |
| `test_login_unknown_user_returns_401_same_message` | HU-004 | Login con email inexistente (mismo mensaje, sin filtrar usuarios) |
| `test_login_inactive_user_returns_403` | HU-004, HU-008 | Login de cuenta desactivada |
| `test_me_requires_token` | HU-005 | Acceso sin token |
| `test_invalid_token_returns_401` | HU-005 | Acceso con JWT malformado |
| `test_reset_password_rejects_unknown_token` | HU-006 | Reset con token inválido |
| `test_reset_password_rejects_reused_token` | HU-006 | Reset con token ya usado |
| `test_create_user_requires_admin` | HU-007 | Creación de usuarios por no-admins |
| `test_admin_cannot_duplicate_email` | HU-007 | Crear dos usuarios con el mismo email |
| `test_admin_cannot_deactivate_self` | HU-008 | Admin desactivándose a sí mismo |
| `test_decode_rejects_tampered_token` | HU-005 | JWT modificado en tránsito |

Estos tests son tan importantes como los "felices": cubren los caminos de error y las restricciones de seguridad del sistema.
