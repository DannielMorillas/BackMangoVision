# BackMangoVision — Backend del Sistema MangoVision

Backend (API REST + capa de modelo IA) del sistema de reconocimiento de enfermedades del Mango Kent mediante Deep Learning.

- **Frontend (UI React):** https://github.com/DannielMorillas/FrontMangoVision
- **Cliente:** ARA Export S.A.C. — Casma / Trujillo, Perú
- **Universidad:** Universidad Privada Antenor Orrego — Facultad de Ingeniería

---

## Estructura del repositorio

```
BackMangoVision/
├── backend/        FastAPI + SQLAlchemy + Alembic (API REST + inferencia)
├── ml/             Notebooks de entrenamiento YOLOv8 / U-Net y artefactos del modelo
├── db/             Scripts SQL de seed (catálogo de enfermedades)
├── docs/           Documentación viva del proyecto, sprints y evidencias
└── docker-compose.yml  (Postgres + MinIO)
```

## Stack técnico

| Capa | Tecnología | Versión objetivo |
|---|---|---|
| API | FastAPI + SQLAlchemy + Alembic | Python 3.11+ (3.12 OK) |
| BD | PostgreSQL | 16 |
| Storage de imágenes | MinIO (compatible S3) | RELEASE.2025 |
| Modelos IA | YOLOv8 (detección) + U-Net (severidad) | Ultralytics 8.x |
| Auth | JWT (HS256, 8h) + bcrypt | python-jose, bcrypt |
| Tests | Pytest | cobertura ≥ 70% |

## Cómo levantar el backend

```powershell
# 1. Variables de entorno
copy .env.example .env

# 2. Postgres + MinIO
docker compose up -d

# 3. Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head

# 4. Seed catálogo + admin inicial (una vez)
docker cp ..\db\seeds\diseases.sql mangovision-postgres:/tmp/diseases.sql
docker exec mangovision-postgres psql -U mangovision -d mangovision -f /tmp/diseases.sql
python scripts/seed_initial_admin.py

# 5. Levantar API
uvicorn app.main:app --reload --port 8000
```

## Documentación SCRUM y evidencias

| Documento | Ruta |
|---|---|
| Roadmap, sprints y backlog | (carpeta paralela `Scrum/` del proyecto académico) |
| Evidencias del Sprint 1 | [docs/sprints/sprint-1/](docs/sprints/sprint-1/) |
| Incidencias resueltas | [docs/sprints/sprint-1/incidencias.md](docs/sprints/sprint-1/incidencias.md) |

## Ramas

- `main` — código estable. Cada PBI cerrado se mergea aquí con su evidencia.
- `develop` — integración del sprint en curso.

## Equipo

| Miembro | Rol Scrum |
|---|---|
| Walter Cueva Chávez | Portfolio Manager / Asesor |
| Patrick Isla | Product Owner / Investigador Principal / Dev |
| Daniel Fabian Morillas Chamache | Project Manager |
| Johan Jhosep Juares Olano | Scrum Master |
