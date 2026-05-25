# Dataset: mango-leaf-disease-cls

| Campo | Valor |
|---|---|
| Fuente | Tipo Kaggle "Mango Leaf Disease Dataset" (clasificación) |
| Formato | Imágenes en carpetas por clase (estilo ImageNet) |
| Tarea original | Clasificación de hoja con enfermedad |
| Bounding boxes | ❌ NO incluidos |

## Inventario

8 clases × 500 imágenes cada una = **4000 imágenes totales**.

| Carpeta | Imágenes | Mapeo a catálogo MangoVision |
|---|---|---|
| `Anthracnose` | 500 | ✅ `antracnosis` (id 1) |
| `Bacterial Canker` | 500 | 🟡 `otras_lesiones` (id 4) |
| `Cutting Weevil` | 500 | 🟡 `otras_lesiones` (id 4) — insecto |
| `Die Back` | 500 | 🟡 `otras_lesiones` (id 4) — muerte regresiva |
| `Gall Midge` | 500 | 🟡 `otras_lesiones` (id 4) — insecto |
| `Healthy` | 500 | ✅ `sano` (id 0) |
| `Powdery Mildew` | 500 | ✅ `oidio` (id 2) — mismo hongo, distinto nombre |
| `Sooty Mould` | 500 | 🟡 `otras_lesiones` (id 4) — hongo negro |

## ⚠️ Limitaciones críticas

1. **Sin bounding boxes:** el dataset es de clasificación, no de detección. Cada imagen tiene una etiqueta pero no la ubicación de la lesión. Para YOLOv8-detect necesitamos bboxes.

2. **Imágenes de HOJA, no de FRUTO:** este es un dataset de **mango leaf disease**. Nuestro proyecto es sobre el **FRUTO** del mango. Síntomas como antracnosis se manifiestan de forma distinta en hoja vs fruto.

3. **Falta `pudricion_peduncular`:** ninguna clase del dataset cubre la pudrición del pedúnculo, que es un PBI del catálogo MangoVision.

## Cómo se puede aprovechar

Opciones (a decidir con el equipo):

**A. Generar pseudo-bboxes y entrenar YOLOv8-detect**
- Para cada imagen, crear un bbox que cubra el 80% central de la imagen.
- Pros: dataset listo, 4000 imágenes balanceadas.
- Cons: bboxes artificiales; el modelo aprenderá a "marcar toda la imagen", no a localizar la lesión.

**B. Entrenar YOLOv8-classification en su lugar**
- Cambiar la arquitectura del modelo. YOLOv8 también soporta clasificación pura.
- Pros: usa el dataset tal cual, sin trampas.
- Cons: el sistema MangoVision pierde la utilidad de **localizar la lesión en el fruto**, que era una funcionalidad clave.

**C. Anotar manualmente un subset con CVAT**
- Tomar 30-50 imágenes por clase relevante, dibujar bboxes manualmente.
- Pros: datos de calidad, formato consistente con Casma.
- Cons: ~200 imágenes anotadas a mano (1-2 días de trabajo del agrónomo).

**D. Descartar este dataset, depender solo de Casma**
- Si las capturas en Casma producen ≥ 150 imágenes/clase, el dataset propio basta.
- Pros: dataset puramente local, sin ruido externo.
- Cons: dependencia total del éxito de las visitas a Casma.

## Decisión pendiente

Esta evidencia se completará cuando el equipo elija una de las opciones A-D arriba. Mientras tanto, las imágenes se conservan aquí.
