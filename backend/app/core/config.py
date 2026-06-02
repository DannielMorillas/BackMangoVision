from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # DB
    database_url: str = Field(alias="DATABASE_URL")

    # JWT
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expires_hours: int = Field(default=8, alias="JWT_EXPIRES_HOURS")
    jwt_reset_expires_hours: int = Field(default=2, alias="JWT_RESET_EXPIRES_HOURS")

    # MinIO
    minio_endpoint: str = Field(default="localhost:9000", alias="MINIO_ENDPOINT")
    minio_root_user: str = Field(default="mangovision", alias="MINIO_ROOT_USER")
    minio_root_password: str = Field(default="changeme_local", alias="MINIO_ROOT_PASSWORD")
    minio_bucket: str = Field(default="images", alias="MINIO_BUCKET")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")

    # Storage: "local" (disco, default dev) o "minio" (produccion S3).
    storage_backend: str = Field(default="local", alias="STORAGE_BACKEND")
    upload_dir: str = Field(default=str(REPO_ROOT / "backend" / "uploads"), alias="UPLOAD_DIR")

    # Modelo IA: ruta al .pt YOLOv8. Si no existe, el servicio corre en modo stub.
    model_path: str = Field(default=str(REPO_ROOT / "ml" / "models" / "custom-v1.pt"), alias="MODEL_PATH")
    # Umbral de aptitud: % de area afectada por encima del cual el fruto es "no apto".
    aptitude_area_threshold: float = Field(default=15.0, alias="APTITUDE_AREA_THRESHOLD")

    # App
    app_env: str = Field(default="development", alias="APP_ENV")
    app_cors_origins: str = Field(default="http://localhost:5173", alias="APP_CORS_ORIGINS")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.app_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
