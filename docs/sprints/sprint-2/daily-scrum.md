# Daily Scrum — Sprint 2
**Sprint Goal:** Tener un dataset híbrido (público + propio) de ≥ 768 imágenes anotadas y dividido en train/val/test, listo para entrenar modelos en Sprint 3.

**Equipo:** Daniel Morillas (PM / Infra) · Johan Juares (SM / Dataset) · Patrick Isla (PO / Captura)
**Período:** 24 – 25 de mayo de 2026

---

## 📅 Día 1 — 24 de mayo de 2026

> *Primer día del Sprint 2. El Sprint Planning se realizó el mismo 24 de mayo luego de cerrar la migración a GitHub del Sprint 1.*

---

### Bootstrap Sprint 2 — Estructura de Datos y Herramientas Auxiliares
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Completé la migración del monorepo local a los dos repositorios GitHub (`BackMangoVision` y `FrontMangoVision`). Los 5 commits del Sprint 1 quedaron con autoría de mi cuenta y ambos repos son accesibles públicamente. También documenté el flujo de trabajo en `docs/git-workflow.md` para que Johan y Patrick puedan alternar autoría en futuros commits desde una sola PC.

**¿Qué vas a lograr hoy?**
- Crear la estructura completa de la carpeta `data/` con sus 11 sub-carpetas (`raw/public/`, `raw/aragroexport/`, `interim/`, `processed/train/val/test/`).
- Actualizar el `.gitignore` para excluir cualquier dato de dataset (`data/raw/`, `data/interim/`, `data/processed/`) y solo versionar `data/README.md`.
- Escribir `scripts/verify_yolo_dataset.py`: validador standalone que detecta labels huérfanos, IDs de clase fuera de rango, coordenadas mal normalizadas y genera distribución ASCII por clase.
- Documentar el setup de CVAT en `cvat/README.md` (instalación, workflow de anotación, mapeo de clases → IDs YOLO).
- Crear el `docs/sprints/sprint-2/README.md` con el plan de 7 PBIs, responsables y Gantt.

**¿Qué impedimentos tienes para lograrlo?**
- Ninguno en la parte de estructura. Una nota: el `.gitignore` anterior tenía caracteres UTF-16 huérfanos al final (producto de un `>>` en PowerShell previo) que causaban warnings en Git. Se reescribirá limpio con secciones comentadas. Esto no bloquea el avance.

---

### EN-002 — Instalar y Configurar CVAT
**Responsable:** Daniel Morillas

**¿Qué lograste ayer?**
- Cerré la migración a GitHub del Sprint 1. El repo `BackMangoVision` está listo con el historial limpio del Sprint 1.

**¿Qué vas a lograr hoy?**
- Clonar el repositorio oficial de CVAT y hacer checkout de la versión `v2.18.0` (congelada para reproducibilidad).
- Levantar los 6 contenedores de CVAT con `docker compose up -d` en una carpeta paralela a `BackMangoVision/`.
- Crear el superusuario de CVAT vía `manage.py createsuperuser`.
- Documentar la decisión arquitectónica de mantener CVAT separado del `docker-compose.yml` principal (CVAT levanta 6 servicios pesados y solo se usa durante la fase de anotación).
- Documentar el mapeo exacto de labels en CVAT → IDs YOLO (orden de creación es crítico): `sano(0)`, `antracnosis(1)`, `oidio(2)`, `pudricion_peduncular(3)`, `otras_lesiones(4)`.

**¿Qué impedimentos tienes para lograrlo?**
- CVAT usa el puerto `8080`. Hay que verificar que no colisione con otros servicios en la máquina (nuestra API es `8000`, Vite `5173`, Postgres `5433`, MinIO `9000/9001`). Si hay conflicto, se puede cambiar el puerto de CVAT via variable de entorno.
- CVAT requiere ~3 GB de RAM libres mientras corre. En sesiones de anotación habrá que hacer `docker compose down` del stack de MangoVision antes de levantar CVAT.
- La ejecución real en la máquina de Daniel queda pendiente para confirmar criterios finales de EN-002 (los contenedores deben estar `Up` y la UI accesible en `localhost:8080`).

---

## 📅 Día 2 — 25 de mayo de 2026

> *La estructura de datos y el setup de CVAT están documentados. Hoy se trabaja en el protocolo de captura y en la importación del dataset público.*

---

### DO-001 — Documentar Protocolo de Captura de Campo (Casma)
**Responsables:** Johan Juares (redacción) · Daniel Morillas (revisión)

**¿Qué lograste ayer?**
- Johan: Participé en el Sprint Planning del día 1 y comencé el borrador del protocolo de captura. Revisé las notas de campo de las 3 sesiones que Patrick realizó en Casma entre marzo y abril de 2026.
- Daniel: Terminé la estructura `data/`, el `.gitignore` actualizado, el script `verify_yolo_dataset.py` y el setup documentado de CVAT v2.18.

**¿Qué vas a lograr hoy?**
- Finalizar y publicar `DO-001.md` con el protocolo completo de captura: equipamiento mínimo, parámetros de captura (distancia, resolución, formato, iluminación), procedimiento paso a paso y estructura de archivos resultante.
- Confirmar las fechas de las 3 sesiones ejecutadas en Casma (primera y última semana de marzo 2026, segunda semana de abril 2026) y documentar el calendario en el protocolo.
- Definir los criterios de aceptación de HU-009 en el mismo documento.

**¿Qué impedimentos tienes para lograrlo?**
- El conteo exacto de fotos por sesión y la ubicación actual de las imágenes depende de Patrick (las fotos están en otra de sus PCs). Hasta que Patrick localice las imágenes y las copie a `data/raw/aragroexport/images/YYYY-MM-DD/`, HU-009 no puede cerrarse al 100%. El protocolo puede finalizarse sin ese dato, documentando los pendientes como acciones de Patrick.

---

### EN-001 — Importar Dataset Público de Mango
**Responsable:** Patrick Isla · Validación: Daniel Morillas

**¿Qué lograste ayer?**
- Participé en el Sprint Planning. Acordamos que yo traería desde mi otra PC los dos datasets públicos que ya tenía descargados: `mango-v1-yolov8` (Roboflow, formato YOLO, 2916 imágenes) y `mango-leaf-disease-cls` (Kaggle, clasificación por carpeta, 4000 imágenes).

**¿Qué vas a lograr hoy?**
- Copiar ambos datasets a `data/raw/public/` con nombres limpios (sin espacios).
- Crear un `SOURCE.md` por dataset con URL de origen, licencia y descripción.
- Ejecutar `scripts/verify_yolo_dataset.py` sobre ambos datasets para obtener el inventario real (conteo de imágenes, bboxes y clases).
- Documentar el hallazgo crítico: ningún dataset coincide al 100% con las 5 clases del sistema MangoVision. En particular, `pudricion_peduncular` no aparece en ninguno de los dos datasets públicos disponibles.
- Presentar las opciones al equipo (A: pseudo-bboxes, B: cambio a clasificación, C: anotación manual, D: solo Casma, E: híbrido) y tomar una decisión con el PO.

**¿Qué impedimentos tienes para lograrlo?**
- El gap entre los datasets públicos y el catálogo de 5 clases del sistema es el impedimento principal de este sprint. Concretamente: `mango-v1-yolov8` tiene clases de maduración (`ripe`/`unripe`), no de enfermedades. `mango-leaf-disease-cls` tiene 8 clases de enfermedades pero sin bounding boxes y sobre hojas, no frutos. La clase `pudricion_peduncular` no tiene representación en ningún dataset público disponible.
- La decisión sobre cómo proceder (Opción E: híbrido pragmático) se tomó hoy mismo con confirmación del PO (Patrick). La estrategia queda documentada en la evidencia de EN-001 y condiciona el resto del Sprint 2.

---

## 📊 Resumen del Sprint 2 (al día 2 — 25 mayo)

| Día | PBIs trabajados | Estado |
|---|---|---|
| Día 1 — 24 mayo | Bootstrap Sprint 2, EN-002 | ✅ Bootstrap completo · 🟡 EN-002 setup documentado, ejecución pendiente en máquina de Daniel |
| Día 2 — 25 mayo | DO-001, EN-001 | ✅ DO-001 protocolo finalizado · 🟡 EN-001 datasets importados, decisión Opción E confirmada |

### PBIs pendientes al cierre de este registro

| ID | Título | Estado | Bloqueador |
|---|---|---|---|
| HU-009 | Realizar Sesiones de Captura en Casma | 🟡 Parcial | Patrick debe localizar y copiar las fotos a `data/raw/aragroexport/` |
| HU-010 | Anotar Imágenes con Bounding Boxes (CVAT → YOLO) | ⏳ Pendiente | Depende de HU-009 (fotos) y EN-002 (CVAT operativo) |
| EN-003 | Dividir Dataset en Train/Val/Test (70/15/15) | ⏳ Pendiente | Depende de HU-010 (anotación completa) |
| EN-004 | Crear y Validar `dataset.yaml` para YOLOv8 | ⏳ Pendiente | Depende de EN-003 (split generado) |

### Decisión clave registrada hoy

> **Opción E — Híbrido pragmático** (confirmada por Patrick Isla, PO, el 25/05/2026):
> - `pudricion_peduncular`: exclusivamente via capturas propias de Casma.
> - `sano`, `antracnosis`, `oidio`, `otras_lesiones`: 30 imágenes/clase de `mango-leaf-disease-cls` anotadas manualmente en CVAT + capturas de Casma.
> - `mango-v1-yolov8`: usado solo como pre-training de localización de fruto (no entra al dataset final).
> - Dataset final estimado: ~320–370 imágenes con bboxes reales + data augmentation x4 ≈ 1480 muestras efectivas.
