# CVAT — Anotación de imágenes (EN-002 + HU-010)

CVAT (Computer Vision Annotation Tool) es la herramienta self-hosted que usamos para anotar bounding boxes en las imágenes capturadas en Casma (HU-009 → HU-010). Exporta directamente al formato YOLO `.txt` que necesita YOLOv8.

> No bakeamos CVAT en nuestro `docker-compose.yml` principal porque solo se usa durante la fase de anotación (Sprint 2). Una vez exportadas las anotaciones, se apaga.

---

## Instalación (una vez por máquina)

```powershell
# 1. Clonar CVAT en una carpeta separada (NO dentro de este repo)
cd c:\
git clone https://github.com/cvat-ai/cvat.git
cd cvat
git checkout v2.18.0   # versión estable a la fecha del Sprint 2

# 2. Configurar host (necesario en Windows)
$env:CVAT_HOST = "localhost"

# 3. Levantar CVAT
docker compose up -d

# 4. Crear superuser (primera vez)
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
# Elige: username = mangovision_admin, email = patrick.isla@..., password = (anota)

# 5. Abrir UI en el navegador
start http://localhost:8080
```

> **Puertos:** CVAT usa el `8080`. Asegúrate que no choque con nada de MangoVision (nuestros puertos son `8000` para la API, `5173` Vite, `55432` Postgres, `9000/9001` MinIO).

## Workflow de anotación

1. **Crear proyecto** en CVAT con las 5 clases (en este orden exacto):

   | ID YOLO | Label name (en CVAT) | Color sugerido |
   |---|---|---|
   | 0 | `sano` | `#22C55E` |
   | 1 | `antracnosis` | `#DC2626` |
   | 2 | `oidio` | `#A855F7` |
   | 3 | `pudricion_peduncular` | `#F97316` |
   | 4 | `otras_lesiones` | `#FACC15` |

2. **Crear tarea** dentro del proyecto, subir las imágenes de `data/raw/aragroexport/images/`.

3. **Anotar** cada imagen dibujando rectángulos sobre las lesiones (o sobre el fruto entero si es `sano`). Una imagen puede tener varias cajas y varias clases.

4. **Validar** una muestra del 10% con el agrónomo de ARA Export antes de exportar.

5. **Exportar** el dataset:
   - Menu del proyecto → **Export dataset** → Format: **YOLO 1.1**.
   - Descomprime el ZIP en `data/raw/aragroexport/labels/`.
   - Verifica con `python ../scripts/verify_yolo_dataset.py data/raw/aragroexport/`.

## Detener CVAT

```powershell
cd c:\cvat
docker compose down
# Los datos quedan persistentes en sus volúmenes nombrados.
```

## Recursos

- Docs oficiales: https://docs.cvat.ai/
- Guía YOLO export: https://docs.cvat.ai/docs/manual/advanced/formats/format-yolo/
- Atajos de teclado de anotación: https://docs.cvat.ai/docs/manual/basics/shortcuts/
