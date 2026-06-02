"""Tests del flujo end-to-end de diagnóstico (EN-010/011/013/014, HU-011/012/013).

Requiere Postgres de test con el catálogo de enfermedades seedeado (igual que el
resto de tests de integración).
"""
import base64

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# PNG 1x1 válido (para que el upload registre dimensiones reales).
PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
)


def _login(make_user) -> str:
    make_user(email="agro@example.com", password="ClaveSegura123")
    resp = client.post(
        "/api/auth/login", json={"email": "agro@example.com", "password": "ClaveSegura123"}
    )
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _upload(token: str, **form) -> dict:
    resp = client.post(
        "/api/imagenes",
        headers=_auth(token),
        files={"file": ("mango.png", PNG_1x1, "image/png")},
        data=form,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestUpload:
    def test_upload_requires_auth(self, clean_users_table):
        resp = client.post(
            "/api/imagenes", files={"file": ("m.png", PNG_1x1, "image/png")}
        )
        assert resp.status_code == 401

    def test_upload_rejects_unsupported_type(self, make_user):
        token = _login(make_user)
        resp = client.post(
            "/api/imagenes",
            headers=_auth(token),
            files={"file": ("m.txt", b"hola", "text/plain")},
        )
        assert resp.status_code == 415

    def test_upload_ok_returns_metadata(self, make_user):
        token = _login(make_user)
        body = _upload(token, lote="L-001", parcela="P-A")
        assert body["id"] > 0
        assert body["original_filename"] == "mango.png"
        assert body["lote"] == "L-001"
        assert body["width"] == 1 and body["height"] == 1


class TestPredictFlow:
    def test_predict_creates_diagnostico(self, make_user):
        token = _login(make_user)
        img = _upload(token)
        resp = client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        assert resp.status_code == 200, resp.text
        diag = resp.json()
        assert diag["mode"] == "stub"
        assert diag["aptitude"] in {"apto", "no_apto"}
        assert len(diag["predictions"]) >= 1
        p = diag["predictions"][0]
        assert p["disease_slug"] and p["disease_color"].startswith("#")
        assert len(p["bbox_xyxy"]) == 4
        assert p["inference_time_ms"] is not None

    def test_predict_is_idempotent(self, make_user):
        token = _login(make_user)
        img = _upload(token)
        first = client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]}).json()
        second = client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]}).json()
        assert len(first["predictions"]) == len(second["predictions"])

    def test_predict_missing_image_404(self, make_user):
        token = _login(make_user)
        resp = client.post("/api/predict", headers=_auth(token), json={"image_id": 999999})
        assert resp.status_code == 404

    def test_get_diagnostico_detail(self, make_user):
        token = _login(make_user)
        img = _upload(token)
        client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        resp = client.get(f"/api/diagnosticos/{img['id']}", headers=_auth(token))
        assert resp.status_code == 200
        assert resp.json()["image"]["id"] == img["id"]


class TestHistorialYResumen:
    def test_list_contains_diagnostico(self, make_user):
        token = _login(make_user)
        img = _upload(token, lote="L-009")
        client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        resp = client.get("/api/diagnosticos", headers=_auth(token))
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] >= 1
        assert any(it["image_id"] == img["id"] for it in body["items"])

    def test_list_filter_by_lote(self, make_user):
        token = _login(make_user)
        img = _upload(token, lote="L-UNICO")
        client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        resp = client.get("/api/diagnosticos?lote=L-UNICO", headers=_auth(token))
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert items and all(it["lote"] == "L-UNICO" for it in items)

    def test_resumen_totals(self, make_user):
        token = _login(make_user)
        img = _upload(token)
        client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        resp = client.get("/api/diagnosticos/resumen", headers=_auth(token))
        assert resp.status_code == 200
        body = resp.json()
        assert body["total_diagnosticos"] >= 1
        assert body["total_detecciones"] >= 1
        assert len(body["por_enfermedad"]) == 5

    def test_metricas(self, make_user):
        token = _login(make_user)
        img = _upload(token)
        client.post("/api/predict", headers=_auth(token), json={"image_id": img["id"]})
        resp = client.get("/api/metricas", headers=_auth(token))
        assert resp.status_code == 200
        body = resp.json()
        assert body["modelo_modo"] == "stub"
        assert body["total_predicciones"] >= 1
        assert len(body["por_enfermedad"]) == 5
