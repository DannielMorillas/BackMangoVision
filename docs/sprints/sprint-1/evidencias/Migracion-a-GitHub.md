# Cierre Sprint 1 — Migración del monorepo local a 2 repos GitHub

| Campo | Valor |
|---|---|
| Tipo | Tarea de cierre de sprint (post-Sprint 1) |
| Sprint | 1 (cierre) |
| Estado | ✅ Done |
| Fecha | 2026-05-24 |
| Responsable | Daniel Morillas (autenticación + push) |

---

## Contexto

Durante el Sprint 1, el código vivió en un único repositorio local `MangoVision/` (monorepo: backend + frontend + docs + db + ml + scripts) sin remoto. Al cierre del Sprint 1 se decidió:

1. **Separar el código en dos repositorios GitHub:**
   - `BackMangoVision` — backend + ml + db + docs + docker-compose.
   - `FrontMangoVision` — frontend (React + Vite + Tailwind).
2. **Atribuir los commits a Daniel Morillas** (gestor del proyecto, dueño de los repos).
3. **Documentar el flujo de trabajo** para que el equipo (Daniel, Johan, Patrick) sepa cómo alternar autoría en commits futuros con una sola PC.

## Decisiones tomadas

| Decisión | Razón |
|---|---|
| División natural Back / Front (no monorepo en GitHub) | El usuario pidió 2 repos. Cada uno con su CI/CD independiente y permisos por equipo. |
| Reescribir autoría de los 5 commits del Sprint 1 a Daniel | Daniel es el dueño de la cuenta GitHub que aloja los repos. Sprint 1 fue inicialización; de Sprint 2 en adelante se alterna por commit. |
| Mantener `MangoVision/` como backup local | Conserva el monorepo original sin tocar, por si hay que volver atrás. |
| URL del remote sin token embebido | El token solo se usa una vez en el push inicial; Windows Credential Manager cachea para los siguientes. |

## Ejecución paso a paso

### Paso 1 — Reescritura de autoría

```bash
cd MangoVision
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
  export GIT_AUTHOR_NAME="Daniel Morillas"
  export GIT_AUTHOR_EMAIL="danielmorillas0@gmail.com"
  export GIT_COMMITTER_NAME="Daniel Morillas"
  export GIT_COMMITTER_EMAIL="danielmorillas0@gmail.com"
' -- --branches
```

Resultado: los 5 commits del Sprint 1 cambiaron de `Patrick Isla <01102001patrickxd@gmail.com>` a `Daniel Morillas <danielmorillas0@gmail.com>`.

### Paso 2 — Split en 2 carpetas

```bash
# BackMangoVision (sin frontend)
cd .. && git clone --quiet MangoVision BackMangoVision
cd BackMangoVision
git remote remove origin
git rm -rq frontend
git -c user.name="Daniel Morillas" -c user.email="danielmorillas0@gmail.com" \
    commit -q -m "split: mover frontend a FrontMangoVision (repo separado)"

# FrontMangoVision (solo frontend)
cd .. && git clone --quiet MangoVision FrontMangoVision
cd FrontMangoVision
git remote remove origin
git rm -rq backend db docs docker-compose.yml .env.example
git -c user.name="Daniel Morillas" -c user.email="danielmorillas0@gmail.com" \
    commit -q -m "split: aislar frontend (backend + docs viven en BackMangoVision)"
```

### Paso 3 — READMEs específicos por repo

- BackMangoVision/README.md: describe backend, enlaza a FrontMangoVision.
- FrontMangoVision/README.md: describe frontend, enlaza a BackMangoVision.

Ambos commiteados con autoría Daniel.

### Paso 4 — Push inicial con token embebido (one-shot)

```bash
git push "https://DannielMorillas:${TOKEN}@github.com/DannielMorillas/BackMangoVision.git" main:main
git push "https://DannielMorillas:${TOKEN}@github.com/DannielMorillas/FrontMangoVision.git" main:main
```

El token se usó **embebido en la URL del comando**, no se guardó en el archivo de configuración del remoto. Tras el push, los remotos quedaron con URL limpia:

```bash
git remote get-url origin
# → https://github.com/DannielMorillas/BackMangoVision.git  (sin token)
```

### Paso 5 — Documentación del flujo

Creado [`docs/git-workflow.md`](../../../git-workflow.md) con:
- Layout local de 2 repos.
- Cómo configurar credenciales en Windows Credential Manager.
- Patrón `git -c user.name="..." -c user.email="..." commit ...` para alternar autoría.
- Convención de mensajes de commit (`<ID>: <descripción>`).
- Cómo agregar colaboradores (Johan, Patrick).

## Estado final

| Repo | URL | Commits totales | Estado |
|---|---|---|---|
| BackMangoVision | https://github.com/DannielMorillas/BackMangoVision | 8 | ✅ Sprint 1 cerrado, Sprint 2 iniciado |
| FrontMangoVision | https://github.com/DannielMorillas/FrontMangoVision | 7 | ✅ Sprint 1 cerrado |

Distribución de commits por autor:

```
Daniel Morillas <danielmorillas0@gmail.com>     |  todos los commits actuales
Johan Juares <juaresojohan@gmail.com>           |  pendientes (Sprint 2 en adelante)
Patrick Isla <01102001patrickxd@gmail.com>      |  pendientes (Sprint 2 en adelante)
```

## Criterios verificados

- [x] Repos GitHub `BackMangoVision` y `FrontMangoVision` accesibles públicamente.
- [x] `git log` muestra todos los commits del Sprint 1 con autor "Daniel Morillas".
- [x] Cada repo tiene su README específico apuntando al otro.
- [x] `git remote get-url origin` no contiene el token en ningún repo.
- [x] `docs/git-workflow.md` publicado con el patrón para futuras sesiones.

## Pendientes (gestión de equipo)

- [ ] Daniel agrega a Johan como colaborador en ambos repos (GitHub → Settings → Collaborators).
- [ ] Daniel agrega a Patrick como colaborador en ambos repos.
- [ ] Johan acepta invitaciones en su cuenta.
- [ ] Patrick acepta invitaciones en su cuenta.
- [ ] Primera prueba: Johan/Patrick clonan y hacen un commit dummy de prueba con su propia autoría.

## Riesgos identificados durante la migración

| Riesgo | Mitigación aplicada |
|---|---|
| Tokens classic pegados en chat → log de la sesión los contiene | Usuario reconoció el riesgo (proyecto académico, repos privados). Recomendado rotarlos al cerrar el proyecto. |
| Antivirus interceptando TLS hace push lento | Documentado en [incidencias.md](incidencias.md#i-05). Usar `NODE_OPTIONS=--use-system-ca` para npm. Git push no tuvo este problema. |
| `MangoVision/` (monorepo backup) puede confundir al equipo | Documentado en git-workflow.md que `MangoVision/` no se modifica más. Se puede eliminar cuando el equipo confirme que todo está en GitHub. |

## Notas para el equipo

- Trabajen **siempre** dentro de `BackMangoVision/` o `FrontMangoVision/`, no en `MangoVision/`.
- Cada PBI = al menos 1 commit con su ID en el mensaje: `EN-001: ...`, `HU-009: ...`.
- Antes de hacer `git commit`, usen la línea con `-c user.name="..." -c user.email="..."` para garantizar autoría correcta.
- Para evitar repetir esa línea, pueden definir 3 funciones de PowerShell (`commit-daniel`, `commit-johan`, `commit-patrick`) en su perfil personal de PowerShell.
