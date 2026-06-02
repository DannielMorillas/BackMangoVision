"""Schemas de administración de modelos y logs de actividad (EN-010, endpoints admin)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MLModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    version: str
    map_at_05: float | None
    file_path: str
    is_active: bool
    trained_at: datetime | None
    created_at: datetime


class MLModelStatusUpdate(BaseModel):
    is_active: bool


class ActivityLogEntry(BaseModel):
    timestamp: datetime
    tipo: str  # login | upload | prediccion | alta_usuario
    descripcion: str
    usuario: str | None = None
