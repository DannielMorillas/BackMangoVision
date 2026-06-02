"""Schemas de imagen, predicción y diagnóstico (Sprint 4)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# --- Imagen ---

class ImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    content_type: str
    size_bytes: int
    width: int | None
    height: int | None
    lote: str | None
    parcela: str | None
    captured_at: datetime | None
    uploaded_at: datetime


# --- Predicción (un bounding box) ---

class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    disease_id: int
    disease_slug: str
    disease_name: str
    disease_color: str
    confidence: float
    bbox_xyxy: list[float]
    severity: str | None
    area_pct: float | None
    inference_time_ms: int | None


# --- Diagnóstico (todas las predicciones de una imagen) ---

class DiagnosticoRead(BaseModel):
    """Detalle completo de un diagnóstico (imagen + detecciones)."""

    image: ImageRead
    predictions: list[PredictionRead]
    is_healthy: bool
    aptitude: str  # apto | no_apto
    model_name: str
    model_version: str
    mode: str  # real | stub
    created_at: datetime


class DiagnosticoListItem(BaseModel):
    """Fila resumida para el historial."""

    image_id: int
    original_filename: str
    lote: str | None
    parcela: str | None
    captured_at: datetime | None
    created_at: datetime
    dominant_disease_slug: str | None
    dominant_disease_name: str | None
    max_confidence: float | None
    n_detections: int
    is_healthy: bool
    aptitude: str


class DiagnosticoListResponse(BaseModel):
    items: list[DiagnosticoListItem]
    total: int
    page: int
    page_size: int


# --- Request de predicción ---

class PredictRequest(BaseModel):
    image_id: int = Field(..., description="ID de una imagen previamente subida vía /api/imagenes")


# --- Dashboard / métricas ---

class DiseaseCount(BaseModel):
    slug: str
    name: str
    color_hex: str
    count: int


class DiagnosticoResumen(BaseModel):
    total_diagnosticos: int
    total_detecciones: int
    apto: int
    no_apto: int
    sanos: int
    por_enfermedad: list[DiseaseCount]
    avg_inference_time_ms: float | None
    ultimos_7_dias: int


class MetricasRead(BaseModel):
    total_imagenes: int
    total_predicciones: int
    por_enfermedad: list[DiseaseCount]
    avg_inference_time_ms: float | None
    p95_inference_time_ms: int | None
    modelo_activo: str
    modelo_modo: str  # real | stub
