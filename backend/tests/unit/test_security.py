import time

import pytest
from jose import JWTError

from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_reset_token,
    hash_password,
    hash_reset_token,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_password_differs_from_plain(self):
        h = hash_password("ClaveSegura123")
        assert h != "ClaveSegura123"
        assert h.startswith("$2b$") or h.startswith("$2a$")

    def test_verify_password_returns_true_on_match(self):
        h = hash_password("ClaveSegura123")
        assert verify_password("ClaveSegura123", h) is True

    def test_verify_password_returns_false_on_mismatch(self):
        h = hash_password("ClaveSegura123")
        assert verify_password("Otra123Distinta", h) is False

    def test_two_hashes_of_same_password_differ_due_to_salt(self):
        assert hash_password("repetida") != hash_password("repetida")


class TestJWT:
    def test_create_and_decode_token_round_trip(self):
        token = create_access_token(subject=42, extra={"role": "admin"})
        payload = decode_access_token(token)
        assert payload["sub"] == "42"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_decode_rejects_tampered_token(self):
        token = create_access_token(subject=1)
        tampered = token + "x"
        with pytest.raises(JWTError):
            decode_access_token(tampered)


class TestResetTokens:
    def test_generate_reset_token_returns_plain_and_hash(self):
        plain, h = generate_reset_token()
        assert len(plain) >= 32
        assert h == hash_reset_token(plain)

    def test_hash_is_deterministic_for_same_input(self):
        assert hash_reset_token("abc") == hash_reset_token("abc")

    def test_hash_changes_with_input(self):
        assert hash_reset_token("abc") != hash_reset_token("abd")

    def test_generated_tokens_are_unique(self):
        a, _ = generate_reset_token()
        b, _ = generate_reset_token()
        assert a != b


@pytest.mark.skip(reason="Cubierto en flujo de login (integration test)")
def test_token_includes_iat_close_to_now():
    now = int(time.time())
    token = create_access_token(subject=1)
    payload = decode_access_token(token)
    assert abs(payload["iat"] - now) < 5
