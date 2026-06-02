"""Métricas globales del sistema (EN-014)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.db import get_db
from app.models import Disease, Image, Prediction, User
from app.schemas.prediction import DiseaseCount, MetricasRead
from app.services.inference import get_inference_service

router = APIRouter(prefix="/api/metricas", tags=["metricas"])


def _percentile(values: list[int], pct: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1)))))
    return ordered[k]


@router.get("", response_model=MetricasRead)
def metricas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MetricasRead:
    diseases = db.query(Disease).all()
    counts = dict(
        db.query(Prediction.disease_id, func.count(Prediction.id))
        .group_by(Prediction.disease_id)
        .all()
    )
    por_enfermedad = [
        DiseaseCount(slug=d.slug, name=d.name, color_hex=d.color_hex, count=int(counts.get(d.id, 0)))
        for d in diseases
    ]

    times = [
        t
        for (t,) in db.query(Prediction.inference_time_ms)
        .filter(Prediction.inference_time_ms.isnot(None))
        .all()
    ]
    avg_time = round(sum(times) / len(times), 1) if times else None

    svc = get_inference_service()
    return MetricasRead(
        total_imagenes=db.query(func.count(Image.id)).scalar() or 0,
        total_predicciones=db.query(func.count(Prediction.id)).scalar() or 0,
        por_enfermedad=por_enfermedad,
        avg_inference_time_ms=avg_time,
        p95_inference_time_ms=_percentile(times, 95),
        modelo_activo=f"{svc.model_name}:{svc.model_version}",
        modelo_modo=svc.mode,
    )
