"""Tests del endpoint /api/diseases (soporte para HU-002)."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_diseases_returns_five_entries():
    response = client.get("/api/diseases")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    slugs = {d["slug"] for d in body}
    expected = {"sano", "antracnosis", "oidio", "pudricion_peduncular", "otras_lesiones"}
    assert expected.issubset(slugs)


def test_each_disease_has_required_fields():
    response = client.get("/api/diseases")
    assert response.status_code == 200
    body = response.json()
    for disease in body:
        for field in ("id", "slug", "name", "color_hex", "description"):
            assert field in disease, f"falta {field} en {disease}"
        assert disease["color_hex"].startswith("#") and len(disease["color_hex"]) == 7


def test_unicode_oidio_returned_correctly():
    response = client.get("/api/diseases")
    oidio = next(d for d in response.json() if d["slug"] == "oidio")
    assert oidio["name"] == "Oídio"
