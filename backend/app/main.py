from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, auth, diseases
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="MangoVision API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diseases.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.get("/api/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}
