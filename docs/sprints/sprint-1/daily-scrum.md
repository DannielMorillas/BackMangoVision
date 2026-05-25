# Daily Scrum — Sprint 1
**Sprint Goal:** Que un ingeniero agrónomo de ARA Export pueda acceder al sistema con credenciales seguras y que la infraestructura técnica esté lista para construir el resto del producto.

**Equipo:** Daniel Morillas (PM / Infra) · Johan Juares (SM / QA) · Patrick Isla (PO / Dev)
**Período:** 22 – 23 de mayo de 2026

---

## 📅 Día 1 — 22 de mayo de 2026

> *Primer día del sprint. El Planning se realizó la tarde del 21 de mayo.*

---

### EN-017 — Instalar Docker, Python y Node.js
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Ayer realizamos el Sprint Planning: refinamos los 14 PBIs, asignamos responsables y estimamos los story points. Quedó claro el orden de ejecución: primero infraestructura (EN-017 a EN-021) y luego las historias de usuario.

**¿Qué vas a lograr hoy?**
- Verificar e instalar Docker, Python y Node.js en la máquina de desarrollo.
- Confirmar versiones instaladas: Docker 24+, Python 3.11+, Node 20+.
- Crear el `docker-compose.yml` base con los servicios PostgreSQL y MinIO.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno crítico. La máquina ya tenía Python 3.12 y Node 24 instalados, que son versiones más recientes que las del plan pero compatibles. Se documentará el desvío en el README para que no genere confusión en revisiones futuras.

---

### EN-018 — Levantar PostgreSQL y MinIO con Docker
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Sprint Planning completado. Se priorizó EN-018 inmediatamente después de EN-017 porque sin la base de datos operativa no se pueden ejecutar las migraciones Alembic.

**¿Qué vas a lograr hoy?**
- Levantar PostgreSQL 16 y MinIO con `docker compose up -d`.
- Crear el bucket `images` automáticamente con el servicio `minio-init`.
- Verificar healthchecks de ambos servicios.

**¿Qué impedimentos tienes para lograrlo?**
- El puerto 5432 de la máquina está ocupado por `wslrelay` (forwarding de WSL2). Se resolverá mapeando el contenedor al puerto externo 5433, ajustando `DATABASE_URL` en `.env` y `.env.example`. No bloquea el avance, solo requiere documentar el desvío.

---

### EN-019 — Configurar Archivo .env con Variables de Entorno
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Sprint Planning listo. El equipo acordó versionar `.env.example` (sin secretos) e ignorar el `.env` real, siguiendo el patrón estándar.

**¿Qué vas a lograr hoy?**
- Crear `.env.example` con todas las variables agrupadas por contexto: PostgreSQL, MinIO, JWT y App.
- Generar el `.env` local con valores de desarrollo.
- Confirmar que `.env` queda excluido de Git con `.gitignore`.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno. Las variables son conocidas desde el plan del proyecto. El único cuidado es no comprometer el `JWT_SECRET` real; se usará un placeholder obvio en el `.env.example`.

---

### EN-020 — Ejecutar Primera Migración Alembic
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Sprint Planning realizado. Se decidió incluir `password_reset_tokens` en la migración inicial para no crear una migración trivial separada cuando se implemente HU-006.

**¿Qué vas a lograr hoy?**
- Escribir los 7 modelos SQLAlchemy (users, diseases, images, predictions, ml_models, manual_labels, password_reset_tokens).
- Autogenerar y revisar manualmente la primera migración Alembic.
- Ejecutar `alembic upgrade head` y verificar que las 7 tablas existen en PostgreSQL.
- Levantar FastAPI con endpoint `/api/health`.

**¿Qué impedimentos tienes para lograrlo?**
- El `alembic/env.py` necesita inyectar `DATABASE_URL` desde `Settings` (Pydantic). Si hay un problema de importación circular al conectar los modelos, puede tomar tiempo de debugging. Se anticipará importando `Base.metadata` directamente en `env.py`.

---

### EN-021 — Insertar Catálogo de Enfermedades
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Sprint Planning completado. El catálogo de 5 clases está definido desde el inicio del proyecto; solo falta materializarlo como seed SQL.

**¿Qué vas a lograr hoy?**
- Escribir `db/seeds/diseases.sql` con `INSERT … ON CONFLICT (slug) DO NOTHING` para que el seed sea idempotente.
- Cargar el seed en la BD con `docker cp` + `psql -f` (evitando el problema de encoding cp1252 de PowerShell).
- Verificar que los 5 slugs y los acentos (Oídio, Pudrición) están bien almacenados.

**¿Qué impedimentos tienes para lograrlo?**
- En Windows, hacer `Get-Content file.sql | docker exec -i psql` corrompe los acentos porque PowerShell interpreta el archivo en cp1252. Se resolverá usando `docker cp` para copiar el archivo al contenedor y luego `psql -f` dentro del contenedor. Se documentará en `db/seeds/README.md` para que el resto del equipo no caiga en la misma trampa.

---

### EN-000 — Crear Repositorio Git con Estructura Completa
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Sprint Planning finalizado. Se acordó trabajar primero sobre un repositorio local y hacer el push a GitHub al cierre del Sprint 1, una vez que el primer end-to-end esté validado.

**¿Qué vas a lograr hoy?**
- Inicializar el repositorio Git con `git init -b main`.
- Crear la estructura completa de carpetas: `backend/`, `frontend/`, `ml/`, `db/`, `docs/`.
- Redactar el `README.md` inicial con propósito, stack e instrucciones de arranque.
- Configurar el `.gitignore` y crear la rama `develop`.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno. La estructura está definida en el plan del proyecto. Se hará el commit inicial en `main` con el mensaje `EN-000: estructura inicial del repo MangoVision`.

---

### HU-001 — Ver Landing Page Informativa
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Sprint Planning completado. Se revisó el beta de la landing y se acordó reescribirla limpia: misma paleta (verde-mango), sin GSAP para esta entrega, conectada al backend real para HU-002.

**¿Qué vas a lograr hoy?**
- Crear el proyecto frontend con Vite + React 19 + Tailwind 4 + React Router 7.
- Implementar la `LandingPage` con secciones: Hero, Beneficios, Enfermedades y CTA final.
- Crear `Navbar`, `Footer` y el tema de colores con CSS custom properties en `@theme`.
- Escribir los tests Vitest básicos de la landing.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno en este momento. Si Tailwind 4 tiene cambios de configuración respecto a la v3 (que usamos en el beta) puede requerir ajustes, pero está documentado en la guía de migración oficial.

---

### HU-002 — Ver Sección de Enfermedades en Landing
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Sprint Planning listo. Se acordó que la sección de enfermedades debe consumir el endpoint `GET /api/diseases` del backend, sin datos hardcoded en el frontend.

**¿Qué vas a lograr hoy?**
- Crear el endpoint `GET /api/diseases` en FastAPI con DTO Pydantic.
- Escribir el servicio `fetchDiseases()` y el componente `DiseaseCard` en el frontend.
- Integrar la sección `#enfermedades` en la `LandingPage` con estado de carga y manejo de error.
- Cubrir con tests de integración (Pytest) y tests de componente (Vitest).

**¿Qué impedimentos tienes para lograrlo?**
- Necesito que EN-020 y EN-021 estén completos (tablas y seed de enfermedades) antes de poder probar el endpoint contra la BD real. Se coordinará con Daniel para ejecutar ambos primero en el día.

---

### HU-003 — Acceder al Sistema desde Landing
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Sprint Planning realizado. Esta historia es relativamente pequeña: tres `<Link to="/login">` y la ruta `/login` registrada en React Router.

**¿Qué vas a lograr hoy?**
- Añadir los tres puntos de entrada a `/login`: Navbar, Hero CTA (`data-testid="cta-primary-login"`) y CTA final.
- Registrar la ruta `/login` en `App.tsx` con un placeholder de `LoginPage`.
- Verificar que la navegación es client-side (sin recarga de página).
- Escribir dos tests Vitest que validen los dos `<Link>` principales.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno. Depende solo de HU-001 (la landing debe existir), que se implementa el mismo día.

---

## 📅 Día 2 — 23 de mayo de 2026

> *Los habilitadores técnicos (EN-017 a EN-021) y la base de la landing (HU-001 a HU-003) están completos. Hoy se cierra el Sprint 1 con las historias de autenticación y gestión de usuarios.*

---

### HU-004 — Iniciar Sesión con Email y Contraseña
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Completé toda la infraestructura técnica (EN-017 a EN-021) junto con Daniel.
- Implementé HU-001 (landing page completa con secciones), HU-002 (sección enfermedades consumiendo `/api/diseases`) y HU-003 (tres CTAs a `/login`). Total: 10 SP cerrados el día 1.

**¿Qué vas a lograr hoy?**
- Implementar `POST /api/auth/login`: verificación de email + bcrypt + validación de `is_active` + emisión de JWT HS256 (8 horas) + actualización de `last_login_at`.
- Crear `LoginPage.tsx` con formulario funcional y `AuthContext` para estado global de sesión.
- Cubrir con 6 tests Pytest y 3 tests Vitest (credenciales válidas, error, must_change_password).

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno. Una nota de implementación: usaré `bcrypt` directamente (no `passlib`) para evitar el bug conocido de `passlib 1.7.4` con `bcrypt 4.x` en Python 3.12. Esto se documenta en las notas técnicas de la evidencia.

---

### HU-005 — Cerrar Sesión del Sistema
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Cerré HU-001, HU-002 y HU-003 (10 SP). La infraestructura completa está operativa.

**¿Qué vas a lograr hoy?**
- Implementar `POST /api/auth/logout` (204 No Content) y `GET /api/auth/me`.
- Crear la dependencia `get_current_user` que valida el JWT en cada request protegido.
- Implementar `ProtectedRoute.tsx` en el frontend para proteger `/dashboard` y `/admin/usuarios`.
- Cubrir con 4 tests Pytest y 5 tests Vitest del guard de ruta.

**¿Qué impedimentos tienes para lograrlo?**
- El criterio de "eliminar el JWT del localStorage" es responsabilidad del frontend. El backend solo provee el endpoint y la dependencia. Hay que asegurar que el flujo de `logout()` en `AuthContext` borre correctamente el token y el estado global.

---

### HU-006 — Recuperar Contraseña Olvidada
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- Landing page completa (HU-001 a HU-003). La infraestructura base está funcionando.

**¿Qué vas a lograr hoy?**
- Implementar el flujo completo de reset: `POST /api/auth/forgot-password` genera un token de 32 bytes (persiste solo el hash SHA-256) con TTL de 2 horas.
- `POST /api/auth/reset-password` valida el token, cambia la contraseña con bcrypt y lo marca como usado.
- En modo `development`, incluir `debug_token` en la respuesta para poder probar sin SMTP.
- Crear `ForgotPasswordPage.tsx` y `ResetPasswordPage.tsx`.
- Cubrir con 5 tests Pytest.

**¿Qué impedimentos tienes para lograrlo?**
- La integración real con SMTP queda pendiente para Sprint 5 (decisión del PO). Hoy se implementa el stub local con `debug_token` que es suficiente para validar el flujo completo en entorno de desarrollo. Hay que asegurarse de que `debug_token` sea `None` en modo `production`.

---

### HU-007 — Crear Cuenta de Ingeniero Agrónomo
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- HU-001 a HU-003 completas. La landing está funcional y conectada al backend.

**¿Qué vas a lograr hoy?**
- Implementar `POST /api/admin/users` protegido con la dependencia `require_admin` (403 si rol ≠ admin).
- El usuario creado lleva `must_change_password=True` para forzar el cambio en el primer login.
- Implementar `AdminUsersPage.tsx` con tabla de usuarios y formulario de creación.
- Crear `scripts/seed_initial_admin.py` para poder tener el primer admin en BD.
- Cubrir con 3 tests Pytest.

**¿Qué impedimentos tienes para lograrlo?**
- Necesito que el seed del admin inicial esté listo antes de poder probar el endpoint manualmente, ya que requiere un token de admin para invocar `POST /api/admin/users`. Esto se resuelve con el script de seed que se ejecuta una sola vez.

---

### HU-008 — Desactivar o Reactivar Cuenta de Usuario
**Responsable:** Patrick Isla

**¿Qué lograste ayer?**
- HU-001 a HU-003 completadas (10 SP en el día 1).

**¿Qué vas a lograr hoy?**
- Implementar `PATCH /api/admin/users/{id}/status` para cambiar el flag `is_active`.
- Agregar la regla de negocio: el admin no puede desactivarse a sí mismo (400).
- Asegurar que la dependencia `get_current_user` rechace tokens de usuarios desactivados (401 inmediato, sin esperar a expiración del JWT).
- Añadir el botón "Activar / Desactivar" en `AdminUsersPage.tsx`.
- Cubrir con 3 tests Pytest.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno. El comportamiento de "token activo de usuario desactivado sigue siendo rechazado" se logra porque `get_current_user` hace `db.get(User, sub)` y verifica `is_active` en cada request. El JWT stateless no requiere blacklist para este caso.

---

## 📅 Día 3 — 24 de mayo de 2026 (Cierre del Sprint)

> *Todos los 14 PBIs del Sprint 1 están completados. Hoy se ejecuta la tarea de cierre: migración del monorepo local a dos repositorios GitHub.*

---

### Migración a GitHub — BackMangoVision y FrontMangoVision
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- El Sprint 1 se cerró con 46/46 SP y 59 tests en verde (41 Pytest + 18 Vitest). La Sprint Review se realizó el 23 de mayo con todos los PBIs aceptados. El código vive todavía en el repositorio local `MangoVision/`.

**¿Qué vas a lograr hoy?**
- Reescribir la autoría de los 5 commits del Sprint 1 a mi cuenta de GitHub (`Daniel Morillas <danielmorillas0@gmail.com>`).
- Hacer el split del monorepo en dos repositorios: `BackMangoVision` (backend + docs + docker) y `FrontMangoVision` (frontend).
- Escribir los READMEs específicos de cada repo y hacer el push inicial a GitHub.
- Documentar el flujo de trabajo en `docs/git-workflow.md` para que Johan y Patrick puedan alternar autoría en sus commits con una sola PC.

**¿Qué impedimentos tienes para lograrlo?**
- El token de acceso a GitHub (Classic PAT) debe generarse con permiso `repo`. Se usará embebido en la URL del `git push` de forma one-shot para no guardarlo en la configuración del remoto. Windows Credential Manager cacheará las credenciales para los pushes siguientes. Se recomienda rotar el token al cerrar el proyecto académico.

---

## 📊 Resumen del Sprint 1

| Día | PBIs cerrados | SP | Responsables |
|---|---|---|---|
| Día 1 — 22 mayo | EN-017, EN-018, EN-019, EN-020, EN-021, EN-000, HU-001, HU-002, HU-003 | 27 | Daniel + Patrick |
| Día 2 — 23 mayo | HU-004, HU-005, HU-006, HU-007, HU-008 | 21 | Patrick |
| Día 3 — 24 mayo | Migración a GitHub | — | Daniel |
| **Total** | **14 PBIs · 46 SP · 59 tests** | **46** | ✅ **Sprint cerrado** |
