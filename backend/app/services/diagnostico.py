"""Construcción de la respuesta de diagnóstico a partir de predicciones persistidas.

Reutilizado por POST /api/predict y GET /api/diagnosticos/{id}.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Disease, Image, MLModel, Prediction
from app.schemas.prediction import DiagnosticoRead, ImageRead, PredictionRead

settings = get_settings()


def _aptitude(predictions: list[Prediction], disease_by_id: dict[int, Disease]) -> str:
    for p in predictions:
        slug = disease_by_id[p.disease_id].slug
        if slug != "sano" and (p.area_pct or 0) >= settings.aptitude_area_threshold:
            return "no_apto"
    return "apto"


def _is_healthy(predictions: list[Prediction], disease_by_id: dict[int, Disease]) -> bool:
    return all(disease_by_id[p.disease_id].slug == "sano" for p in predictions)


def build_diagnostico(db: Session, image: Image) -> DiagnosticoRead:
    predictions = (
        db.query(Prediction)
        .filter(Prediction.image_id == image.id)
        .order_by(Prediction.confidence.desc())
        .all()
    )
    disease_by_id = {d.id: d for d in db.query(Disease).all()}

    pred_reads: list[PredictionRead] = []
    model_id: int | None = None
    for p in predictions:
        d = disease_by_id[p.disease_id]
        model_id = p.model_id
        pred_reads.append(
            PredictionRead(
                id=p.id,
                disease_id=p.disease_id,
                disease_slug=d.slug,
                disease_name=d.name,
                disease_color=d.color_hex,
                confidence=p.confidence,
                bbox_xyxy=p.bbox_xyxy,
                severity=p.severity,
                area_pct=p.area_pct,
                inference_time_ms=p.inference_time_ms,
            )
        )

    model = db.get(MLModel, model_id) if model_id is not None else None
    model_name = model.name if model else "desconocido"
    model_version = model.version if model else "—"
    mode = "stub" if model_name.startswith("stub") else "real"
    created_at = max((p.created_at for p in predictions), default=image.uploaded_at)

    return DiagnosticoRead(
        image=ImageRead.model_validate(image),
        predictions=pred_reads,
        is_healthy=_is_healthy(predictions, disease_by_id) if predictions else True,
        aptitude=_aptitude(predictions, disease_by_id),
        model_name=model_name,
        model_version=model_version,
        mode=mode,
        created_at=created_at,
    )
