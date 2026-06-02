"""Tests de los endpoints admin/models, admin/logs y diagnosticos/export (EN-010)."""
import base64

from fastapi.testclient import TestClient

from app.main import app
from app.models import MLModel, UserRole

client = TestClient(app)

PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M8AAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
)


def _login(make_user, email: str, role: UserRole) -> str:
    make_user(email=email, password="ClaveSegura123", role=role)
    resp = client.post("/api/auth/login", json={"email": email, "password": "ClaveSegura123"})
    return resp.json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


class TestAdminModels:
    def test_models_requires_admin(self, make_user):
        token = _login(make_user, "agro@example.com", UserRole.AGRONOMIST)
        assert client.get("/api/admin/models", headers=_auth(token)).status_code == 403

    def test_admin_lists_and_activates_model(self, make_user, db_session):
        token = _login(make_user, "admin@example.com", UserRole.ADMIN)
        m = MLModel(name="custom-v1", version="v1", file_path="ml/models/custom-v1.pt", is_active=False)
        db_session.add(m)
        db_session.commit()
        db_session.refresh(m)

        listing = client.get("/api/admin/models", headers=_auth(token))
        assert listing.status_code == 200
        assert any(item["id"] == m.id for item in listing.json())

        patched = client.patch(
            f"/api/admin/models/{m.id}", headers=_auth(token), json={"is_active": True}
        )
        assert patched.status_code == 200
        assert patched.json()["is_active"] is True

    def test_patch_unknown_model_404(self, make_user):
        token = _login(make_user, "admin@example.com", UserRole.ADMIN)
        resp = client.patch("/api/admin/models/999999", headers=_auth(token), json={"is_active": True})
        assert resp.status_code == 404


class TestAdminLogs:
    def test_logs_requires_admin(self, make_user):
        token = _login(make_user, "agro@example.com", UserRole.AGRONOMIST)
        assert client.get("/api/admin/logs", headers=_auth(token)).status_code == 403

    def test_logs_returns_entries(self, make_user):
        token = _login(make_user, "admin@example.com", UserRole.ADMIN)
        resp = client.get("/api/admin/logs", headers=_auth(token))
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        # Debe incluir el alta del propio admin.
        assert any(e["tipo"] == "alta_usuario" and "admin@example.com" in e["descripcion"] for e in body)


class TestExportCsv:
    def test_export_returns_csv(self, make_user):
        token = _login(make_user, "agro@example.com", UserRole.AGRONOMIST)
        up = client.post(
            "/api/imagenes",
            headers=_auth(token),
            files={"file": ("m.png", PNG_1x1, "image/png")},
            data={"lote": "L-EXP"},
        )
        image_id = up.json()["id"]
        client.post("/api/predict", headers=_auth(token), json={"image_id": image_id})

        resp = client.get("/api/diagnosticos/export", headers=_auth(token))
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/csv")
        lines = resp.text.strip().splitlines()
        assert lines[0].startswith("image_id,archivo,lote,parcela")
        assert any(str(image_id) in line for line in lines[1:])
