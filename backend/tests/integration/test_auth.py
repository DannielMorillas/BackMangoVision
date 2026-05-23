"""Tests del flujo de autenticación (HU-004, HU-005, HU-006)."""
from fastapi.testclient import TestClient

from app.core.security import decode_access_token
from app.main import app
from app.models import UserRole

client = TestClient(app)


# ---------- HU-004 Login ----------

class TestLogin:
    def test_login_ok_returns_jwt_and_user(self, make_user):
        make_user(email="ada@example.com", password="ClaveSegura123")
        resp = client.post(
            "/api/auth/login",
            json={"email": "ada@example.com", "password": "ClaveSegura123"},
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["token_type"] == "bearer"
        assert body["expires_in_seconds"] == 8 * 3600
        assert body["user"]["email"] == "ada@example.com"

        payload = decode_access_token(body["access_token"])
        assert payload["sub"] == str(body["user"]["id"])
        assert payload["role"] == "agronomist"

    def test_login_email_is_case_insensitive(self, make_user):
        make_user(email="ada@example.com", password="ClaveSegura123")
        resp = client.post(
            "/api/auth/login",
            json={"email": "ADA@example.com", "password": "ClaveSegura123"},
        )
        assert resp.status_code == 200

    def test_login_wrong_password_returns_401(self, make_user):
        make_user(email="ada@example.com", password="ClaveSegura123")
        resp = client.post(
            "/api/auth/login",
            json={"email": "ada@example.com", "password": "Incorrecta"},
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Credenciales inválidas"

    def test_login_unknown_user_returns_401_same_message(self, clean_users_table):
        resp = client.post(
            "/api/auth/login",
            json={"email": "nadie@example.com", "password": "lo-que-sea"},
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Credenciales inválidas"

    def test_login_inactive_user_returns_403(self, make_user):
        make_user(email="off@example.com", password="ClaveSegura123", is_active=False)
        resp = client.post(
            "/api/auth/login",
            json={"email": "off@example.com", "password": "ClaveSegura123"},
        )
        assert resp.status_code == 403

    def test_login_updates_last_login_at(self, make_user, db_session):
        u = make_user(email="ada@example.com", password="ClaveSegura123")
        assert u.last_login_at is None
        client.post(
            "/api/auth/login",
            json={"email": "ada@example.com", "password": "ClaveSegura123"},
        )
        db_session.refresh(u)
        assert u.last_login_at is not None


# ---------- HU-005 Logout / /me / guard ----------

class TestLogoutAndMe:
    def _login(self, email: str, password: str) -> str:
        resp = client.post("/api/auth/login", json={"email": email, "password": password})
        return resp.json()["access_token"]

    def test_me_requires_token(self, clean_users_table):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_me_returns_current_user(self, make_user):
        make_user(email="me@example.com", password="ClaveSegura123")
        token = self._login("me@example.com", "ClaveSegura123")
        resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "me@example.com"

    def test_logout_returns_204(self, make_user):
        make_user(email="me@example.com", password="ClaveSegura123")
        token = self._login("me@example.com", "ClaveSegura123")
        resp = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 204

    def test_invalid_token_returns_401(self, clean_users_table):
        resp = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-jwt"})
        assert resp.status_code == 401


# ---------- HU-006 Forgot/reset password ----------

class TestForgotResetPassword:
    def test_forgot_password_returns_200_even_if_unknown_user(self, clean_users_table):
        resp = client.post(
            "/api/auth/forgot-password",
            json={"email": "ghost@example.com"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "se enviará un enlace" in body["message"]
        assert body.get("debug_token") is None

    def test_forgot_password_returns_debug_token_in_dev(self, make_user):
        make_user(email="forget@example.com", password="ClaveSegura123")
        resp = client.post(
            "/api/auth/forgot-password",
            json={"email": "forget@example.com"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("debug_token") and len(body["debug_token"]) >= 32
        assert body.get("debug_expires_at")

    def test_reset_password_changes_credential(self, make_user):
        make_user(email="reset@example.com", password="ClaveSegura123")
        body = client.post(
            "/api/auth/forgot-password",
            json={"email": "reset@example.com"},
        ).json()
        token = body["debug_token"]

        resp = client.post(
            "/api/auth/reset-password",
            json={"token": token, "new_password": "NuevaClave456"},
        )
        assert resp.status_code == 204

        # vieja no funciona, nueva sí
        old = client.post(
            "/api/auth/login",
            json={"email": "reset@example.com", "password": "ClaveSegura123"},
        )
        assert old.status_code == 401
        new = client.post(
            "/api/auth/login",
            json={"email": "reset@example.com", "password": "NuevaClave456"},
        )
        assert new.status_code == 200

    def test_reset_password_rejects_unknown_token(self, clean_users_table):
        resp = client.post(
            "/api/auth/reset-password",
            json={"token": "x" * 40, "new_password": "NuevaClave456"},
        )
        assert resp.status_code == 400

    def test_reset_password_rejects_reused_token(self, make_user):
        make_user(email="reuse@example.com", password="ClaveSegura123")
        token = client.post(
            "/api/auth/forgot-password",
            json={"email": "reuse@example.com"},
        ).json()["debug_token"]

        ok = client.post(
            "/api/auth/reset-password",
            json={"token": token, "new_password": "NuevaClave456"},
        )
        assert ok.status_code == 204

        repeat = client.post(
            "/api/auth/reset-password",
            json={"token": token, "new_password": "OtraClave789"},
        )
        assert repeat.status_code == 400


# ---------- HU-007/HU-008 Admin ----------

class TestAdminUsers:
    def _login(self, email: str, password: str) -> str:
        resp = client.post("/api/auth/login", json={"email": email, "password": password})
        return resp.json()["access_token"]

    def test_create_user_requires_admin(self, make_user):
        make_user(email="agronomo@example.com", password="ClaveSegura123")
        token = self._login("agronomo@example.com", "ClaveSegura123")

        resp = client.post(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": "nuevo@example.com",
                "first_name": "Nuevo",
                "last_name": "Agronomo",
                "role": "agronomist",
                "temp_password": "Temporal123",
            },
        )
        assert resp.status_code == 403

    def test_admin_creates_user_must_change_password(self, make_user):
        make_user(email="admin@example.com", password="AdminClave123", role=UserRole.ADMIN)
        token = self._login("admin@example.com", "AdminClave123")

        resp = client.post(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": "nuevo@example.com",
                "first_name": "Nuevo",
                "last_name": "Agronomo",
                "role": "agronomist",
                "temp_password": "Temporal123",
            },
        )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["email"] == "nuevo@example.com"
        assert body["must_change_password"] is True
        assert body["is_active"] is True

        # El usuario nuevo puede loguearse con la contraseña temporal
        login = client.post(
            "/api/auth/login",
            json={"email": "nuevo@example.com", "password": "Temporal123"},
        )
        assert login.status_code == 200

    def test_admin_cannot_duplicate_email(self, make_user):
        make_user(email="admin@example.com", password="AdminClave123", role=UserRole.ADMIN)
        make_user(email="ada@example.com", password="ClaveSegura123")
        token = self._login("admin@example.com", "AdminClave123")

        resp = client.post(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": "ada@example.com",
                "first_name": "x",
                "last_name": "y",
                "role": "agronomist",
                "temp_password": "Temporal123",
            },
        )
        assert resp.status_code == 409

    def test_admin_deactivates_user_and_user_cannot_login(self, make_user, db_session):
        make_user(email="admin@example.com", password="AdminClave123", role=UserRole.ADMIN)
        target = make_user(email="objetivo@example.com", password="ClaveSegura123")
        token = self._login("admin@example.com", "AdminClave123")

        resp = client.patch(
            f"/api/admin/users/{target.id}/status",
            headers={"Authorization": f"Bearer {token}"},
            json={"is_active": False},
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

        login = client.post(
            "/api/auth/login",
            json={"email": "objetivo@example.com", "password": "ClaveSegura123"},
        )
        assert login.status_code == 403

    def test_admin_cannot_deactivate_self(self, make_user):
        admin = make_user(email="admin@example.com", password="AdminClave123", role=UserRole.ADMIN)
        token = self._login("admin@example.com", "AdminClave123")

        resp = client.patch(
            f"/api/admin/users/{admin.id}/status",
            headers={"Authorization": f"Bearer {token}"},
            json={"is_active": False},
        )
        assert resp.status_code == 400

    def test_admin_reactivates_user(self, make_user):
        make_user(email="admin@example.com", password="AdminClave123", role=UserRole.ADMIN)
        target = make_user(
            email="objetivo@example.com", password="ClaveSegura123", is_active=False
        )
        token = self._login("admin@example.com", "AdminClave123")

        resp = client.patch(
            f"/api/admin/users/{target.id}/status",
            headers={"Authorization": f"Bearer {token}"},
            json={"is_active": True},
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is True

        login = client.post(
            "/api/auth/login",
            json={"email": "objetivo@example.com", "password": "ClaveSegura123"},
        )
        assert login.status_code == 200
