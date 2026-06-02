# HU-009 — Plan de Captura en Etapa de Fruto (sesión adicional)

| Campo | Valor |
|---|---|
| Deriva de | Decisión PO 2026-06-01 (HU-009 § 8) |
| Objetivo | Capturar ~200 imágenes de **fruto** Kent para cubrir el catálogo de enfermedades del modelo |
| Protocolo base | [DO-001.md](DO-001.md) (parámetros de captura siguen vigentes) |
| Estado | ⏳ Por programar (fecha según fenología del lote) |

---

## 1. Contexto y riesgo de cronograma (leer primero)

Las fotos ya recibidas son de **floración** (mayo 2026). El catálogo objetivo necesita **fruto** (antracnosis, pudrición peduncular). En Casma/Áncang la fructificación del Kent ocurre **meses después** de la floración (campaña de exportación peruana ≈ dic–mar).

➡️ **Implicación honesta:** esta sesión puede caer **fuera de la ventana del Sprint 3** y posiblemente del roadmap de 14 semanas. Por eso:

- **No se bloquea el Sprint 3:** el baseline YOLOv8 se entrena **ya** con el dataset público (`mango-v1-yolov8`, 2041 img). Ver `scripts/train_yolo.py`.
- El dataset de fruto propio entra como **iteración posterior (EN-006)** / mejora continua, o como aporte para la **validación con usuarios reales (Sprint 5, HU-016)**.
- Si la campaña de fruto no llega a tiempo para la tesis, el sustento es: *"el modelo se validó con dataset público + set real de floración Casma; la ampliación a fruto queda como trabajo futuro / segunda iteración."*

## 2. Objetivo de la sesión

| Métrica | Meta |
|---|---|
| Imágenes de fruto | ≥ 200 (mínimo 40 por clase) |
| Clases a cubrir | `sano`, `antracnosis`, `pudricion_peduncular`, `otras_lesiones` |
| Calidad | Cumplir § 3 de DO-001 (distancia 15–30 cm, ≥12 MP, JPG, enfoque sobre lesión) |
| Validación | Agrónomo ARA Export clasifica/confirma in situ (≥10%) |

## 3. Qué fotografiar (checklist de campo)

- [ ] **Fruto sano** en árbol y cosechado (fondo neutro) — 40+.
- [ ] **Antracnosis:** manchas oscuras circulares hundidas en cáscara — 40+.
- [ ] **Pudrición peduncular:** oscurecimiento desde la zona del pedúnculo — 40+.
- [ ] **Otras lesiones:** daño mecánico, quemadura de sol, picadura de mosca de la fruta — 40+.
- [ ] 3 ángulos por fruto con lesión (frente / lateral / cenital).
- [ ] Fotos con referencia de escala (tarjeta 5 cm) en una fracción de las tomas.

## 4. Logística

| Item | Detalle |
|---|---|
| Coordinación | Confirmar con Dpto. Control Fitosanitario ARA Export la **parcela con mayor incidencia** de antracnosis |
| Ventana horaria | 08:00–11:00 y 15:00–17:00 (evitar sol cenital 11–15) |
| Equipo | Smartphone ≥12 MP, power bank, cartulina neutra A3, tarjeta de escala, planilla/tablet |
| Geolocalización | Mantener app Timemark activa (ya se usó en la sesión de floración) |
| Backup | Transferir a PC la misma noche + subir a MinIO |

## 5. Al volver del campo (integración al repo)

1. Copiar a `data/raw/aragroexport/images/` con prefijo `casma_<fecha>_fruto_NNN.jpg`.
2. Registrar en `manifest.csv` con `categoria=fruto`, `clase_tentativa`, `lote`, `parcela`.
3. Anotar en CVAT (HU-010) → exportar YOLO a `labels/`.
4. `python scripts/verify_yolo_dataset.py` para integridad.
5. `python scripts/split_dataset.py` para mezclar público + propio (floración + fruto).

## 6. Mientras tanto (acción inmediata, no esperar la visita)

- [ ] **EN-005 baseline:** correr `split_dataset.py` sobre el dataset público y entrenar YOLOv8n (Colab/Kaggle). Esto cierra el bloqueo de Sprint 3 sin depender de la visita de fruto.
- [ ] **HU-010 floración:** anotar las 27 candidatas de Casma (cenicilla + malformación) como set de validación de dominio real.
