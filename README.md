# MangoVision

Sistema de Reconocimiento de Enfermedades del Mango Kent mediante Deep Learning.

**Cliente:** ARA Export S.A.C. — Casma / Trujillo, Perú
**Universidad:** Universidad Privada Antenor Orrego — Facultad de Ingeniería

---

## Estructura del repositorio

```
MangoVision/
├── backend/        FastAPI + SQLAlchemy + Alembic (API REST + inferencia)
├── frontend/       React + Vite + Ant Design (UI)
├── ml/             Notebooks de entrenamiento YOLOv8 / U-Net y artefactos del modelo
├── db/             Scripts SQL de seed y catálogo de enfermedades
├── docs/           Documentación viva del proyecto, sprints y evidencias
└── docker-compose.yml
```

## Stack técnico

| Capa | Tecnología | Versión objetivo |
|---|---|---|
| Frontend | React + Vite + TypeScript + Ant Design | React 19, Vite 8 |
| Backend | FastAPI + SQLAlchemy + Alembic | Python 3.11+ (3.12 OK) |
| BD | PostgreSQL | 16 |
| Storage de imágenes | MinIO (compatible S3) | RELEASE.2025 |
| Modelos IA | YOLOv8 (detección) + U-Net (severidad) | Ultralytics 8.x |
| Auth | JWT (HS256, 8h) + bcrypt | python-jose, passlib |
| Tests | Pytest (backend), Vitest (frontend) | cobertura ≥ 70% |

## Cómo levantar el entorno (desarrollo)

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Levantar Postgres + MinIO
docker compose up -d postgres minio

# 3. Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 4. Frontend
cd ../frontend
npm install
npm run dev
```

## Documentación SCRUM

La gestión del proyecto (sprints, historias, métricas) está en `../Scrum/`.
Las evidencias de cada HU/EN cerrado están en `docs/sprints/sprint-N/evidencias/`.

## Ramas

- `main` — código estable, releases.
- `develop` — integración continua del sprint en curso.
- Feature branches: `feature/HU-XXX-titulo-corto`.
