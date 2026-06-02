# Candidatas a anotación en CVAT — HU-010

> Selección derivada de [`data/raw/aragroexport/manifest.csv`](../../../../data/raw/aragroexport/manifest.csv) (visita Casma, 52 fotos).
> Total candidatas: **27** (11 alta + 16 media) + 4 opcionales.
> Fuente de imágenes: `data/raw/aragroexport/images/`.

## Clases tentativas a usar en CVAT

Ajustadas al material real observado (predomina floración, no fruto):

| Clase CVAT | Descripción | Mapea a catálogo |
|---|---|---|
| `malformacion_floral` | Yema/escoba de bruja, brote deformado, agalla | (nueva — floración) |
| `cenicilla` | Polvillo blanco-grisáceo en botones/panícula | `oidio` |
| `necrosis_panicula` | Inflorescencia seca/necrosada | `otras_lesiones` |
| `sano` | Tejido sin síntoma (para balance negativo) | `sano` |

> Definir las clases finales **con el agrónomo de ARA Export** antes de anotar (validación del 10% según criterio de Sprint 2).

## Prioridad ALTA — síntoma macro nítido (11)

Estas son las de mayor valor: close-ups enfocados de síntoma. Anotar primero.

| Archivo | Síntoma aparente |
|---|---|
| casma_2026-05-25_006.jpg | Yema/agalla ennegrecida |
| casma_2026-05-25_010.jpg | Yema con agalla + exudado + insectos |
| casma_2026-05-25_012.jpg | Yema con malformación |
| casma_2026-05-25_022.jpg | Botones florales con necrosis/malformación |
| casma_2026-05-25_028.jpg | Botones deformados / malformación floral |
| casma_2026-05-25_030.jpg | Yema con agalla (escoba) + necrosis en hoja |
| casma_2026-05-25_035.jpg | Yema con agalla y exudado + insectos |
| casma_2026-05-25_038.jpg | Yema con malformación (escoba) + necrosis |
| casma_2026-05-25_047.jpg | Yema con cenicilla (polvillo blanco) |
| casma_2026-05-25_048.jpg | Yema con malformación (escoba) y necrosis |
| casma_2026-05-25_050.jpg | Cenicilla marcada en botones (macro) |

## Prioridad MEDIA — panícula / toma media (16)

| Archivo | Síntoma aparente |
|---|---|
| casma_2026-05-25_002.jpg | Cenicilla/necrosis en panícula |
| casma_2026-05-25_004.jpg | Inflorescencia necrosada |
| casma_2026-05-25_009.jpg | Inflorescencia necrosada |
| casma_2026-05-25_011.jpg | Cenicilla en panícula |
| casma_2026-05-25_018.jpg | Manchas oscuras (fumagina/cenicilla) |
| casma_2026-05-25_019.jpg | Cenicilla (polvillo blanco) |
| casma_2026-05-25_023.jpg | Inflorescencia seca con frutos pequeños |
| casma_2026-05-25_024.jpg | Inflorescencia |
| casma_2026-05-25_025.jpg | Inflorescencia necrosada |
| casma_2026-05-25_032.jpg | Cenicilla |
| casma_2026-05-25_036.jpg | Inflorescencia necrosada (en mano) |
| casma_2026-05-25_037.jpg | Cenicilla |
| casma_2026-05-25_041.jpg | Inflorescencia seca |
| casma_2026-05-25_043.jpg | Cenicilla |
| casma_2026-05-25_044.jpg | Cenicilla |
| casma_2026-05-25_046.jpg | Inflorescencia (contrapicado) |

## Prioridad BAJA — opcional (4)

Anotar solo si se necesita balance de la clase `sano` o ejemplos de síntoma leve.

| Archivo | Contenido |
|---|---|
| casma_2026-05-25_007.jpg | Brote nuevo (mayormente sano) |
| casma_2026-05-25_021.jpg | Hojas (síntoma leve) |
| casma_2026-05-25_026.jpg | Brote floral con puntas de hoja necrosadas |
| casma_2026-05-25_042.jpg | Inflorescencia joven (en mano, sana) |

## Excluidas de anotación (25)

- **Árbol/panorámica (4):** `_016`, `_029`, `_034`, `_051` — sin escala de síntoma.
- **Contexto/manejo (17):** personas, fumigación, deshierbe, trampas — sirven como **evidencia de visita HU-009**, no para entrenar.
- (El resto ya está en las tablas de arriba.)

## Flujo HU-010 sugerido

1. Crear proyecto en CVAT con las clases acordadas (§ "Clases tentativas").
2. Subir las **27 candidatas** (alta + media).
3. Anotar bounding boxes; agrónomo valida el 10%.
4. Exportar en formato **YOLO 1.1** → `data/raw/aragroexport/labels/`.
5. Verificar integridad con `scripts/verify_yolo_dataset.py`.
6. Re-ejecutar `scripts/split_dataset.py` para mezclar con el dataset público.
