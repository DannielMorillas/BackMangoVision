"""Subida y descarga de imágenes (EN-010 / HU-012)."""
from __future__ import annotations

import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.db import get_db
from app.models import Image, User
from app.schemas.prediction import ImageRead
from app.services import storage

router = APIRouter(prefix="/api/imagenes", tags=["imagenes"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}
MAX_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB


def _read_dimensions(data: bytes) -> tuple[int | None, int | None]:
    try:
        from PIL import Image as PILImage

        with PILImage.open(io.BytesIO(data)) as img:
            return img.width, img.height
    except Exception:
        return None, None


@router.post("", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
def upload_image(
    file: UploadFile = File(...),
    lote: str | None = Form(default=None),
    parcela: str | None = Form(default=None),
    captured_at: datetime | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Image:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Tipo no soportado: {file.content_type}. Use JPEG/PNG/WEBP/BMP.",
        )
    data = file.file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Archivo vacío")
    if len(data) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen supera el máximo de {MAX_SIZE_BYTES // (1024 * 1024)} MB",
        )

    width, height = _read_dimensions(data)
    object_key = storage.build_object_key(file.filename or "imagen.jpg")
    storage.get_storage().save(data, object_key, file.content_type)

    image = Image(
        user_id=current_user.id,
        object_key=object_key,
        original_filename=file.filename or "imagen.jpg",
        content_type=file.content_type,
        size_bytes=len(data),
        width=width,
        height=height,
        lote=lote,
        parcela=parcela,
        captured_at=captured_at,
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.get("/{image_id}/contenido")
def get_image_content(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    image = db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    try:
        data = storage.get_storage().load(image.object_key)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no disponible")
    return Response(content=data, media_type=image.content_type)
