"""Servicio de inferencia de enfermedades sobre imágenes de mango.

Diseñado para funcionar en DOS modos, transparentes para el resto del backend:

  - **real**: si `ultralytics` está instalado Y existe el archivo del modelo (`MODEL_PATH`),
    carga el YOLOv8 una sola vez (singleton) y ejecuta inferencia real.
  - **stub**: si falta cualquiera de los dos, genera detecciones *deterministas* a partir
    del hash de la imagen. Permite construir y demostrar todo el sistema end-to-end
    (upload → predict → dashboard) ANTES de tener el modelo entrenado (EN-006).

Cuando el `.pt` real exista, basta con instalarlo en `MODEL_PATH` y reinstalar
`ultralytics`: el servicio cambia a modo real sin tocar endpoints ni frontend.

Mapeo de clases: el índice de clase del modelo corresponde, por orden, al catálogo
MangoVision (ver `CLASS_SLUGS`). Debe coincidir con `scripts/split_dataset.py`.
"""
from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass
from pathlib import Path

from app.core.config import get_settings

settings = get_settings()

# Orden = índice de clase YOLO. Idéntico a CLASS_NAMES de scripts/split_dataset.py.
CLASS_SLUGS = ["sano", "antracnosis", "oidio", "pudricion_peduncular", "otras_lesiones"]


@dataclass
class Detection:
    class_index: int
    class_slug: str
    confidence: float
    bbox_xyxy: list[float]  # coords en píxeles [x1, y1, x2, y2]
    severity: str | None
    area_pct: float | None


@dataclass
class InferenceResult:
    detections: list[Detection]
    inference_time_ms: int
    model_name: str
    model_version: str
    mode: str  # "real" | "stub"

    @property
    def is_healthy(self) -> bool:
        """True si no se detectó ninguna enfermedad (solo 'sano' o sin detecciones)."""
        return all(d.class_slug == "sano" for d in self.detections)

    @property
    def aptitude(self) -> str:
        """'apto' / 'no_apto' según el umbral de área afectada configurado."""
        for d in self.detections:
            if d.class_slug != "sano" and (d.area_pct or 0) >= settings.aptitude_area_threshold:
                return "no_apto"
        return "apto"


def severity_from_area(area_pct: float | None) -> str | None:
    if area_pct is None:
        return None
    if area_pct < 10:
        return "leve"
    if area_pct < 30:
        return "moderado"
    return "severo"


class InferenceService:
    """Singleton: carga el modelo una vez y resuelve cada inferencia."""

    def __init__(self) -> None:
        self._model = None
        self.mode = "stub"
        self.model_name = "stub-detector"
        self.model_version = "stub-0"
        self._try_load_real_model()

    def _try_load_real_model(self) -> None:
        model_file = Path(settings.model_path)
        if not model_file.is_file():
            return
        try:
            from ultralytics import YOLO  # import perezoso
        except ImportError:
            return
        self._model = YOLO(str(model_file))
        self.mode = "real"
        self.model_name = model_file.stem
        self.model_version = model_file.stem

    # --- Inferencia ---

    def predict(self, image_bytes: bytes, width: int, height: int) -> InferenceResult:
        start = time.perf_counter()
        if self.mode == "real" and self._model is not None:
            detections = self._predict_real(image_bytes, width, height)
        else:
            detections = self._predict_stub(image_bytes, width, height)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return InferenceResult(
            detections=detections,
            inference_time_ms=elapsed_ms,
            model_name=self.model_name,
            model_version=self.model_version,
            mode=self.mode,
        )

    def _predict_real(self, image_bytes: bytes, width: int, height: int) -> list[Detection]:
        import numpy as np
        from PIL import Image as PILImage

        img = PILImage.open(__import__("io").BytesIO(image_bytes)).convert("RGB")
        results = self._model(np.asarray(img), verbose=False)
        detections: list[Detection] = []
        for r in results:
            boxes = getattr(r, "boxes", None)
            if boxes is None:
                continue
            for box in boxes:
                cls_idx = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = (float(v) for v in box.xyxy[0].tolist())
                area_pct = round(((x2 - x1) * (y2 - y1)) / max(1.0, width * height) * 100, 2)
                slug = CLASS_SLUGS[cls_idx] if 0 <= cls_idx < len(CLASS_SLUGS) else "otras_lesiones"
                detections.append(
                    Detection(
                        class_index=cls_idx,
                        class_slug=slug,
                        confidence=round(conf, 4),
                        bbox_xyxy=[round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
                        severity=severity_from_area(area_pct) if slug != "sano" else None,
                        area_pct=area_pct if slug != "sano" else None,
                    )
                )
        return detections

    def _predict_stub(self, image_bytes: bytes, width: int, height: int) -> list[Detection]:
        """Detecciones deterministas derivadas del hash de la imagen.

        La misma imagen siempre produce el mismo resultado → demos y tests estables.
        """
        seed = int(hashlib.sha256(image_bytes).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)

        n = rng.choices([1, 2, 3], weights=[0.5, 0.35, 0.15])[0]
        detections: list[Detection] = []
        for _ in range(n):
            # Clase sesgada hacia enfermedades para que las demos muestren diagnóstico.
            class_index = rng.choices(range(len(CLASS_SLUGS)), weights=[0.2, 0.3, 0.2, 0.15, 0.15])[0]
            slug = CLASS_SLUGS[class_index]

            bw = rng.uniform(0.15, 0.4) * width
            bh = rng.uniform(0.15, 0.4) * height
            x1 = rng.uniform(0, max(1.0, width - bw))
            y1 = rng.uniform(0, max(1.0, height - bh))
            x2, y2 = x1 + bw, y1 + bh

            confidence = round(rng.uniform(0.62, 0.96), 4)
            if slug == "sano":
                area_pct = None
                severity = None
            else:
                area_pct = round(rng.uniform(4, 38), 2)
                severity = severity_from_area(area_pct)

            detections.append(
                Detection(
                    class_index=class_index,
                    class_slug=slug,
                    confidence=confidence,
                    bbox_xyxy=[round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
                    severity=severity,
                    area_pct=area_pct,
                )
            )
        return detections


_service: InferenceService | None = None


def get_inference_service() -> InferenceService:
    global _service
    if _service is None:
        _service = InferenceService()
    return _service
