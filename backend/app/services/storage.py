"""Almacenamiento de imágenes subidas.

Dos backends seleccionables vía `STORAGE_BACKEND`:
    - "local" (default): guarda en disco bajo `UPLOAD_DIR`. Cero dependencias de infra,
      ideal para desarrollo, demos y tests.
    - "minio": guarda en MinIO/S3 (producción). Requiere el servicio MinIO levantado.

La interfaz pública es estable (`save`, `load`, `public_ref`) para que el resto del
backend no dependa del backend concreto.
"""
from __future__ import annotations

import io
import uuid
from datetime import date
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()


def build_object_key(original_filename: str) -> str:
    """Genera una key única estable: imagenes/YYYY/MM/DD/<uuid>.<ext>."""
    ext = Path(original_filename).suffix.lower() or ".jpg"
    today = date.today()
    return f"imagenes/{today:%Y/%m/%d}/{uuid.uuid4().hex}{ext}"


class _LocalStorage:
    """Guarda bajo UPLOAD_DIR. `object_key` se usa como ruta relativa."""

    def __init__(self, root: str) -> None:
        self.root = Path(root)

    def save(self, data: bytes, object_key: str, content_type: str) -> None:  # noqa: ARG002
        dest = self.root / object_key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    def load(self, object_key: str) -> bytes:
        return (self.root / object_key).read_bytes()

    def public_ref(self, object_key: str) -> str:
        # En local servimos vía el endpoint /api/imagenes/{id}/contenido.
        return object_key


class _MinioStorage:
    """Guarda en un bucket MinIO/S3. Import perezoso para no exigir el paquete en dev."""

    def __init__(self) -> None:
        from minio import Minio  # import perezoso

        self._client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=settings.minio_secure,
        )
        self._bucket = settings.minio_bucket
        if not self._client.bucket_exists(self._bucket):
            self._client.make_bucket(self._bucket)

    def save(self, data: bytes, object_key: str, content_type: str) -> None:
        self._client.put_object(
            self._bucket,
            object_key,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )

    def load(self, object_key: str) -> bytes:
        resp = self._client.get_object(self._bucket, object_key)
        try:
            return resp.read()
        finally:
            resp.close()
            resp.release_conn()

    def public_ref(self, object_key: str) -> str:
        return f"{self._bucket}/{object_key}"


def _build_backend():
    if settings.storage_backend.lower() == "minio":
        return _MinioStorage()
    return _LocalStorage(settings.upload_dir)


# Singleton del backend activo.
_backend = None


def get_storage():
    global _backend
    if _backend is None:
        _backend = _build_backend()
    return _backend
