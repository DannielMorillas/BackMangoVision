import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings

_settings = get_settings()


# ---------- Passwords (bcrypt) ----------

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


# ---------- JWT ----------

def create_access_token(subject: str | int, extra: dict | None = None) -> str:
    expires_delta = timedelta(hours=_settings.jwt_expires_hours)
    now = datetime.now(timezone.utc)
    payload: dict = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": "access",
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, _settings.jwt_secret, algorithm=_settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decodifica un JWT y devuelve el payload. Lanza JWTError si es inválido o expirado."""
    return jwt.decode(token, _settings.jwt_secret, algorithms=[_settings.jwt_algorithm])


# ---------- Reset tokens (para HU-006) ----------

def generate_reset_token() -> tuple[str, str]:
    """Devuelve (token_plain, token_hash). Solo el hash se persiste."""
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return token, token_hash


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


__all__ = [
    "JWTError",
    "create_access_token",
    "decode_access_token",
    "generate_reset_token",
    "hash_password",
    "hash_reset_token",
    "verify_password",
]
