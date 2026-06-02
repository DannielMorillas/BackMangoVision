"""Historial y resumen de diagnósticos (HU-011 / HU-014)."""
from __future__ import annotations

import csv
import io
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.db import get_db
from app.models import Disease, Image, Prediction, User
from app.schemas.prediction import (
    DiagnosticoListItem,
    DiagnosticoListResponse,
    DiagnosticoRead,
    DiagnosticoResumen,
    DiseaseCount,
)
from app.services.diagnostico import build_diagnostico

router = APIRouter(prefix="/api/diagnosticos", tags=["diagnosticos"])
settings = get_settings()


def _classify(preds: list[Prediction], disease_by_id: dict[int, Disease]):
    """Devuelve (dominant_disease, max_conf, n, is_healthy, aptitude) para una imagen."""
    if not preds:
        return None, None, 0, True, "apto"
    top = max(preds, key=lambda p: p.confidence)
    dominant = disease_by_id[top.disease_id]
    is_healthy = all(disease_by_id[p.disease_id].slug == "sano" for p in preds)
    aptitude = "apto"
    for p in preds:
        if disease_by_id[p.disease_id].slug != "sano" and (p.area_pct or 0) >= settings.aptitude_area_threshold:
            aptitude = "no_apto"
            break
    return dominant, top.confidence, len(preds), is_healthy, aptitude


@router.get("/resumen", response_model=DiagnosticoResumen)
def resumen(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticoResumen:
    disease_by_id = {d.id: d for d in db.query(Disease).all()}
    preds = db.query(Prediction).all()

    by_image: dict[int, list[Prediction]] = {}
    for p in preds:
        by_image.setdefault(p.image_id, []).append(p)

    apto = no_apto = sanos = 0
    for plist in by_image.values():
        _, _, _, is_healthy, aptitude = _classify(plist, disease_by_id)
        if is_healthy:
            sanos += 1
        if aptitude == "apto":
            apto += 1
        else:
            no_apto += 1

    counts: dict[int, int] = {}
    for p in preds:
        counts[p.disease_id] = counts.get(p.disease_id, 0) + 1
    por_enfermedad = [
        DiseaseCount(slug=d.slug, name=d.name, color_hex=d.color_hex, count=counts.get(d.id, 0))
        for d in disease_by_id.values()
    ]

    avg_time = (
        db.query(func.avg(Prediction.inference_time_ms))
        .filter(Prediction.inference_time_ms.isnot(None))
        .scalar()
    )
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent = {p.image_id for p in preds if p.created_at and p.created_at.replace(tzinfo=None) >= week_ago}

    return DiagnosticoResumen(
        total_diagnosticos=len(by_image),
        total_detecciones=len(preds),
        apto=apto,
        no_apto=no_apto,
        sanos=sanos,
        por_enfermedad=por_enfermedad,
        avg_inference_time_ms=round(float(avg_time), 1) if avg_time is not None else None,
        ultimos_7_dias=len(recent),
    )


def _collect_items(
    db: Session,
    disease: str | None,
    lote: str | None,
    parcela: str | None,
    aptitude: str | None,
) -> list[DiagnosticoListItem]:
    """Lista (sin paginar) de diagnósticos aplicando filtros. Reutilizada por list y export."""
    disease_by_id = {d.id: d for d in db.query(Disease).all()}

    img_q = (
        db.query(Image)
        .filter(Image.id.in_(db.query(Prediction.image_id).distinct()))
        .order_by(Image.uploaded_at.desc())
    )
    if lote:
        img_q = img_q.filter(Image.lote == lote)
    if parcela:
        img_q = img_q.filter(Image.parcela == parcela)
    images = img_q.all()

    preds = db.query(Prediction).filter(Prediction.image_id.in_([i.id for i in images] or [0])).all()
    by_image: dict[int, list[Prediction]] = {}
    for p in preds:
        by_image.setdefault(p.image_id, []).append(p)

    items: list[DiagnosticoListItem] = []
    for img in images:
        plist = by_image.get(img.id, [])
        dominant, max_conf, n, is_healthy, apt = _classify(plist, disease_by_id)
        if disease and (dominant is None or dominant.slug != disease):
            continue
        if aptitude and apt != aptitude:
            continue
        items.append(
            DiagnosticoListItem(
                image_id=img.id,
                original_filename=img.original_filename,
                lote=img.lote,
                parcela=img.parcela,
                captured_at=img.captured_at,
                created_at=max((p.created_at for p in plist), default=img.uploaded_at),
                dominant_disease_slug=dominant.slug if dominant else None,
                dominant_disease_name=dominant.name if dominant else None,
                max_confidence=max_conf,
                n_detections=n,
                is_healthy=is_healthy,
                aptitude=apt,
            )
        )
    return items


@router.get("", response_model=DiagnosticoListResponse)
def list_diagnosticos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    disease: str | None = Query(default=None, description="Filtrar por slug de enfermedad dominante"),
    lote: str | None = Query(default=None),
    parcela: str | None = Query(default=None),
    aptitude: str | None = Query(default=None, pattern="^(apto|no_apto)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> DiagnosticoListResponse:
    items = _collect_items(db, disease, lote, parcela, aptitude)
    total = len(items)
    start = (page - 1) * page_size
    page_items = items[start : start + page_size]
    return DiagnosticoListResponse(items=page_items, total=total, page=page, page_size=page_size)


@router.get("/export")
def export_diagnosticos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    disease: str | None = Query(default=None),
    lote: str | None = Query(default=None),
    parcela: str | None = Query(default=None),
    aptitude: str | None = Query(default=None, pattern="^(apto|no_apto)$"),
) -> Response:
    """Exporta el historial filtrado a CSV (HU-014 / Project Charter)."""
    items = _collect_items(db, disease, lote, parcela, aptitude)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        ["image_id", "archivo", "lote", "parcela", "enfermedad_dominante",
         "confianza", "n_detecciones", "aptitud", "sano", "fecha"]
    )
    for it in items:
        writer.writerow([
            it.image_id,
            it.original_filename,
            it.lote or "",
            it.parcela or "",
            it.dominant_disease_name or "",
            f"{it.max_confidence:.4f}" if it.max_confidence is not None else "",
            it.n_detections,
            it.aptitude,
            "si" if it.is_healthy else "no",
            it.created_at.isoformat(),
        ])
    csv_text = buf.getvalue()
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="diagnosticos.csv"'},
    )


@router.get("/{image_id}", response_model=DiagnosticoRead)
def get_diagnostico(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DiagnosticoRead:
    image = db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
    return build_diagnostico(db, image)
