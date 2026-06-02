"""Inferencia sobre una imagen subida (EN-011 / HU-013)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.db import get_db
from app.models import Disease, Image, MLModel, Prediction, User
from app.schemas.prediction import DiagnosticoRead, PredictRequest
from app.services.diagnostico import build_diagnostico
from app.services.inference import InferenceService, get_inference_service

router = APIRouter(prefix="/api/predict", tags=["predict"])


def _get_or_create_model(db: Session, svc: InferenceService) -> MLModel:
    """Devuelve la fila ml_models que representa al modelo activo (la crea si falta)."""
    model = (
        db.query(MLModel)
        .filter(MLModel.name == svc.model_name, MLModel.version == svc.model_version)
        .first()
    )
    if model is None:
        model = MLModel(
            name=svc.model_name,
            version=svc.model_version,
            file_path="(stub)" if svc.mode == "stub" else svc.model_name,
            is_active=True,
        )
        db.add(model)
        db.commit()
        db.refresh(model)
    return model


@router.post("", response_model=DiagnosticoRead)
def predict(
    payload: PredictRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    svc: InferenceService = Depends(get_inference_service),
) -> DiagnosticoRead:
    image = db.get(Image, payload.image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")

    # Idempotencia simple: si ya hay predicciones para esta imagen, devolver el diagnóstico existente.
    already = db.query(Prediction).filter(Prediction.image_id == image.id).first()
    if already is not None:
        return build_diagnostico(db, image)

    from app.services import storage

    try:
        data = storage.get_storage().load(image.object_key)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contenido de la imagen no disponible"
        )

    result = svc.predict(data, image.width or 640, image.height or 640)
    model = _get_or_create_model(db, svc)
    disease_by_slug = {d.slug: d for d in db.query(Disease).all()}
    if not disease_by_slug:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Catálogo de enfermedades vacío. Ejecutar db/seeds/diseases.sql.",
        )

    for det in result.detections:
        disease = disease_by_slug.get(det.class_slug) or disease_by_slug.get("otras_lesiones")
        db.add(
            Prediction(
                image_id=image.id,
                model_id=model.id,
                disease_id=disease.id,
                confidence=det.confidence,
                bbox_xyxy=det.bbox_xyxy,
                severity=det.severity,
                area_pct=det.area_pct,
                inference_time_ms=result.inference_time_ms,
            )
        )
    db.commit()
    return build_diagnostico(db, image)
