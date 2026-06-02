"""Tests del servicio de inferencia en modo stub (EN-011)."""
from app.services.inference import (
    CLASS_SLUGS,
    InferenceService,
    severity_from_area,
)


def test_class_slugs_match_catalog_order():
    assert CLASS_SLUGS == ["sano", "antracnosis", "oidio", "pudricion_peduncular", "otras_lesiones"]


def test_severity_thresholds():
    assert severity_from_area(None) is None
    assert severity_from_area(5) == "leve"
    assert severity_from_area(9.9) == "leve"
    assert severity_from_area(10) == "moderado"
    assert severity_from_area(29.9) == "moderado"
    assert severity_from_area(30) == "severo"
    assert severity_from_area(80) == "severo"


def test_stub_is_deterministic():
    svc = InferenceService()
    assert svc.mode == "stub"  # sin modelo .pt instalado
    data = b"imagen-de-prueba-12345"
    r1 = svc.predict(data, 640, 480)
    r2 = svc.predict(data, 640, 480)
    assert [d.bbox_xyxy for d in r1.detections] == [d.bbox_xyxy for d in r2.detections]
    assert [d.class_slug for d in r1.detections] == [d.class_slug for d in r2.detections]


def test_stub_detections_are_valid():
    svc = InferenceService()
    w, h = 800, 600
    result = svc.predict(b"otra-imagen", w, h)
    assert 1 <= len(result.detections) <= 3
    assert result.inference_time_ms >= 0
    for d in result.detections:
        assert d.class_slug in CLASS_SLUGS
        x1, y1, x2, y2 = d.bbox_xyxy
        assert 0 <= x1 < x2 <= w
        assert 0 <= y1 < y2 <= h
        assert 0.0 <= d.confidence <= 1.0
        if d.class_slug == "sano":
            assert d.area_pct is None and d.severity is None
        else:
            assert d.area_pct is not None and d.severity in {"leve", "moderado", "severo"}


def test_different_images_can_differ():
    svc = InferenceService()
    a = svc.predict(b"aaaa", 640, 640)
    b = svc.predict(b"zzzz-distinta", 640, 640)
    # No es garantía absoluta, pero con hashes distintos casi siempre difieren en algo.
    assert (
        [d.class_slug for d in a.detections] != [d.class_slug for d in b.detections]
        or [d.bbox_xyxy for d in a.detections] != [d.bbox_xyxy for d in b.detections]
    )
