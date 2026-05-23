"""Tests de integración de la infraestructura (EN-018, EN-020, EN-021).

Requieren que el stack Docker esté arriba (`docker compose up -d`).
"""
from sqlalchemy import text


def test_database_connection(db_session):
    """EN-018: la BD acepta conexiones."""
    result = db_session.execute(text("SELECT 1")).scalar_one()
    assert result == 1


def test_all_seven_tables_exist(db_session):
    """EN-020: las 7 tablas del esquema inicial existen."""
    expected = {
        "users",
        "diseases",
        "images",
        "ml_models",
        "predictions",
        "manual_labels",
        "password_reset_tokens",
    }
    rows = db_session.execute(
        text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
        )
    ).all()
    actual = {row[0] for row in rows}
    missing = expected - actual
    assert not missing, f"Faltan tablas: {missing}"


def test_alembic_version_recorded(db_session):
    """EN-020: alembic_version registró una migración aplicada."""
    rows = db_session.execute(text("SELECT version_num FROM alembic_version")).all()
    assert len(rows) == 1, "Debería haber exactamente una versión registrada"
    assert rows[0][0], "version_num no debe ser vacío"


def test_disease_catalog_has_five_entries(db_session):
    """EN-021: el catálogo de enfermedades tiene las 5 clases del plan."""
    expected_slugs = {
        "sano",
        "antracnosis",
        "oidio",
        "pudricion_peduncular",
        "otras_lesiones",
    }
    rows = db_session.execute(text("SELECT slug FROM diseases")).all()
    actual = {row[0] for row in rows}
    assert actual == expected_slugs, f"Slugs en BD: {actual} vs esperados {expected_slugs}"


def test_disease_records_have_required_fields(db_session):
    """EN-021: cada registro tiene name, color_hex y description no vacíos."""
    rows = db_session.execute(
        text("SELECT slug, name, color_hex, description FROM diseases")
    ).all()
    assert len(rows) >= 5
    for slug, name, color_hex, description in rows:
        assert name and name.strip(), f"name vacío en {slug}"
        assert color_hex.startswith("#") and len(color_hex) == 7, f"color_hex inválido en {slug}"
        assert description and description.strip(), f"description vacía en {slug}"


def test_unicode_preserved_in_disease_names(db_session):
    """EN-021: los nombres con acentos se guardan correctamente en UTF-8."""
    name = db_session.execute(
        text("SELECT name FROM diseases WHERE slug = 'oidio'")
    ).scalar_one()
    assert name == "Oídio", f"UTF-8 corrompido: {name!r}"
