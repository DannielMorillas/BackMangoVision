# `data/` — Carpeta de datasets de MangoVision

Esta carpeta contiene los datasets crudos, intermedios y procesados del proyecto.

> ⚠️ **Importante:** el contenido pesado (imágenes y labels) **NO se versiona en Git**. Solo este `README.md` y la convención de carpetas viajan en el repo. Cada miembro del equipo descarga / copia los datos siguiendo este documento.

---

## Estructura esperada

```
data/
├── README.md                        ← este archivo (versionado)
├── raw/                             ← datos sin tocar (gitignored)
│   ├── public/                      ← dataset público (Kaggle / Roboflow)
│   │   ├── images/                  ← *.jpg / *.png
│   │   └── labels/                  ← *.txt (formato YOLO)
│   └── aragroexport/                ← capturas propias en Casma (HU-009)
│       ├── images/                  ← fotos del smartphone
│       ├── labels/                  ← anotaciones CVAT exportadas (HU-010)
│       └── metadata.csv             ← fecha, hora, zona, lote, parcela por imagen
├── interim/                         ← deduplicación, limpieza, conversiones
└── processed/                       ← dataset final consumido por YOLOv8
    ├── train/
    │   ├── images/
    │   └── labels/
    ├── val/
    │   ├── images/
    │   └── labels/
    ├── test/
    │   ├── images/
    │   └── labels/
    └── dataset.yaml                 ← configuración YOLO (EN-004)
```

---

## Mapeo de clases (Catálogo MangoVision)

El sistema reconoce exactamente **5 clases**, en este orden (importante para los IDs YOLO):

| ID YOLO | slug | Nombre | Color |
|---|---|---|---|
| `0` | `sano` | Fruto sano | `#22C55E` (verde) |
| `1` | `antracnosis` | Antracnosis | `#DC2626` (rojo) |
| `2` | `oidio` | Oídio | `#A855F7` (morado) |
| `3` | `pudricion_peduncular` | Pudrición del pedúnculo | `#F97316` (naranja) |
| `4` | `otras_lesiones` | Otras lesiones | `#FACC15` (amarillo) |

Si el dataset público tiene otro ordenamiento, hay que **remapear los IDs** antes de copiarlo aquí. Usaremos el script `scripts/remap_yolo_classes.py` (EN-001) para esto.

---

## Pasos para integrar el dataset público que ya existe (EN-001)

1. **Copia las imágenes** del dataset público a:
   ```
   data/raw/public/images/    ← todos los .jpg / .png
   data/raw/public/labels/    ← todos los .txt YOLO
   ```
2. Si las clases del dataset original no están ordenadas como nuestro catálogo:
   - Crea `data/raw/public/classes_original.txt` con el orden original.
   - Ejecuta el script de remap (lo crearé en EN-001).
3. Documenta la fuente en `data/raw/public/SOURCE.md`:
   - URL del dataset
   - Licencia
   - Conteo de imágenes y labels
   - Cómo se descargó

---

## Pasos para las capturas propias de Casma (HU-009)

1. Captura con smartphone ≥ 12 MP siguiendo [protocolo DO-001](../docs/sprints/sprint-2/evidencias/DO-001.md).
2. Descarga las fotos a `data/raw/aragroexport/images/`.
3. Crea `data/raw/aragroexport/metadata.csv` con columnas:
   ```
   filename,date,time,zone,lote,parcela,notes
   IMG_001.jpg,2026-05-30,09:15,Norte,L-001,P-A,fruto en arbol
   ```
4. Anota las imágenes en CVAT (HU-010) — exporta a YOLO en `data/raw/aragroexport/labels/`.

---

## Splits Train/Val/Test (EN-003)

Una vez que `raw/public/` + `raw/aragroexport/` están listos, ejecutar el splitter:

```powershell
cd backend
python ../scripts/split_dataset.py --train 0.7 --val 0.15 --test 0.15
```

El script lee de `raw/`, mezcla los dos orígenes manteniendo balance por clase, y produce `processed/{train,val,test}/{images,labels}/`.

---

## Resumen ejecutivo (qué hace el equipo)

| Acción | Archivos involucrados | Responsable | PBI |
|---|---|---|---|
| Copiar dataset público YOLO a `raw/public/` | imágenes + labels .txt | Patrick (transferencia desde otra PC) | EN-001 |
| Setup CVAT con Docker | `cvat/docker-compose.yml` | Daniel (ejecuta) | EN-002 |
| Capturar imágenes en Casma | smartphone + DO-001 | Patrick + agrónomo | HU-009 |
| Anotar imágenes propias en CVAT | exportar YOLO a `raw/aragroexport/labels/` | Patrick | HU-010 |
| Validación cruzada del 10% | revisión visual | Agrónomo de ARA Export | HU-010 |
| Splitter train/val/test | script Python | Daniel / Johan | EN-003 |
| Generar `dataset.yaml` | YAML para YOLOv8 | Daniel / Johan | EN-004 |
