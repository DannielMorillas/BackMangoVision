# Flujo de trabajo con Git — BackMangoVision + FrontMangoVision

Este documento explica cómo el equipo (Daniel Morillas, Johan Juares, Patrick Isla) trabaja con los dos repos en paralelo, atribuyendo correctamente la autoría de cada commit aun cuando se desarrolla desde una sola PC.

---

## 1. Layout local

```
notion/                          (carpeta del proyecto académico)
├── BackMangoVision/             ← clon de github.com/DannielMorillas/BackMangoVision
│   ├── backend/  ml/  db/  docs/  docker-compose.yml
│   └── .git/
└── FrontMangoVision/            ← clon de github.com/DannielMorillas/FrontMangoVision
    ├── frontend/
    └── .git/
```

`MangoVision/` (el monorepo original) se conserva como backup local de Sprint 1. **No se modifica más.** Todo el trabajo de Sprint 2 en adelante ocurre en `BackMangoVision/` o `FrontMangoVision/`.

---

## 2. Configurar credenciales (una sola vez por máquina)

Al primer `git push` después del clone, Git pedirá usuario + password vía Windows Credential Manager. Pega el **token** como password.

```powershell
# Por máquina: garantiza que Windows Credential Manager esté activo
git config --global credential.helper manager

# (Opcional) Identidad por defecto local — sirve solo si no usas -c por commit
git config --global user.name "Patrick Isla"
git config --global user.email "01102001patrickxd@gmail.com"
```

> **Si Windows Credential Manager popup no aparece (terminal sin GUI):** alternativa rápida es pushear una vez embebiendo el token en la URL:
> ```powershell
> git push https://DannielMorillas:TU_TOKEN@github.com/DannielMorillas/BackMangoVision.git main
> ```
> Después del primer push exitoso, el remoto sigue siendo el normal y los siguientes push reutilizan la sesión.

---

## 3. Hacer commits con autoría correcta (sin cambiar config global)

La autoría se controla **por commit**, no por push. Patrón estándar:

```powershell
# Commit como Daniel
git -c user.name="Daniel Morillas" -c user.email="danielmorillas0@gmail.com" `
    commit -m "EN-001: descargar dataset publico de mango"

# Commit como Johan
git -c user.name="Johan Juares" -c user.email="juaresojohan@gmail.com" `
    commit -m "EN-002: instalar y configurar CVAT"

# Commit como Patrick
git -c user.name="Patrick Isla" -c user.email="01102001patrickxd@gmail.com" `
    commit -m "HU-010: anotar imagenes con bounding boxes"
```

GitHub muestra el avatar del autor si el email coincide con uno verificado en la cuenta de GitHub. Si no, muestra el nombre sin avatar enlazado (igual queda atribuido correctamente).

### Alias útiles (opcional)

Agrega en `~/.gitconfig` o ejecuta una vez:

```powershell
git config --global alias.daniel "-c user.name=Daniel Morillas -c user.email=danielmorillas0@gmail.com"
git config --global alias.johan  "-c user.name=Johan Juares -c user.email=juaresojohan@gmail.com"
git config --global alias.patrick "-c user.name=Patrick Isla -c user.email=01102001patrickxd@gmail.com"
```

> ⚠️ Git no soporta alias con espacios en valores directamente; los alias de arriba pueden fallar en ciertos shells. La forma segura sigue siendo la línea completa con `-c`.

Alternativa más simple: scripts PowerShell `commit-daniel.ps1`, `commit-johan.ps1`, etc. (uno por persona).

---

## 4. Pushing — quién autentica

- **Daniel** es el owner de ambos repos. Su token autentica los push sin más.
- **Johan** y **Patrick** necesitan que Daniel los agregue como colaboradores:
  - Repo en GitHub → **Settings** → **Collaborators** → **Add people** → buscar por usuario o email.
  - Aceptar la invitación en la cuenta del colaborador.
- Una vez son colaboradores, pueden usar su propio token para pushear.

El **autor del commit y quien pushea son independientes**. Cualquiera del equipo puede pushear un commit cuyo autor sea otro miembro — lo importante es que la autoría refleje quién hizo el trabajo.

---

## 5. Convención de commits por PBI

Una historia / habilitador / tarea = **un commit** (al menos uno; varios si la tarea es grande):

```
<ID>: <verbo en presente o pasado> <qué se hizo>
```

Ejemplos:
- `EN-001: descargar dataset publico de Kaggle Mango Disease`
- `HU-009: completar primera sesion de captura en Casma (84 imagenes)`
- `EN-003: dividir dataset en 70/15/15 train/val/test`
- `RN-001: validar mAP@0.5 0.87 en test set`

En el cuerpo del commit (línea en blanco + texto), puedes referenciar la evidencia:

```
EN-001: descargar dataset publico de Kaggle Mango Disease

- Fuente: kaggle.com/datasets/.../mango-leaf-disease
- 4000 imagenes, 8 clases (descartamos 3)
- Guardado en data/raw/public/
- Evidencia: docs/sprints/sprint-2/evidencias/EN-001.md
```

---

## 6. Ramas

| Rama | Uso |
|---|---|
| `main` | Estable. Cada PBI cerrado se mergea aquí. |
| `develop` | Integración del sprint en curso (creada en Sprint 1). |
| `feature/<ID>-<slug>` | Trabajo de un PBI específico. Se mergea a `develop` cuando pasa tests. |

Para el equipo actual (4 personas, proyecto académico), trabajar directo en `develop` y mergear a `main` al cierre del sprint es práctica suficiente.

---

## 7. Sincronización entre repos

Si una HU toca backend y frontend (típico de Sprint 4 en adelante), se hace **un commit por repo**, ambos referenciando el mismo ID:

- En `BackMangoVision`: `HU-012: endpoint POST /api/imagenes con multipart`
- En `FrontMangoVision`: `HU-012: componente UploadImage con drag & drop`

Ambos commits pueden referirse a la misma evidencia (que vive en `BackMangoVision/docs/sprints/sprint-4/evidencias/HU-012.md`).
