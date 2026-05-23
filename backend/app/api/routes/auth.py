from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.db import get_db
from app.core.security import (
    create_access_token,
    generate_reset_token,
    hash_password,
    hash_reset_token,
    verify_password,
)
from app.models import PasswordResetToken, User
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.schemas.user import UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])
_settings = get_settings()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta está desactivada. Contacte al administrador.",
        )

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, extra={"role": user.role.value})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_seconds=_settings.jwt_expires_hours * 3600,
        user=UserRead.model_validate(user),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_user: User = Depends(get_current_user)) -> None:
    """
    JWT es stateless: el logout se hace en el cliente borrando el token.
    Este endpoint existe para que el frontend tenga un punto de llamada explícito
    y para preparar el camino a una blacklist/refresh-token en el futuro.
    """
    return None


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    payload: ForgotPasswordRequest, db: Session = Depends(get_db)
) -> ForgotPasswordResponse:
    """
    Genera un token de reseteo si el usuario existe. SIEMPRE devuelve 200
    con un mensaje genérico para no filtrar qué emails están registrados.

    En modo desarrollo (APP_ENV=development) la respuesta incluye el token
    plano en `debug_token` para poder probar el flujo sin SMTP configurado.
    """
    email = payload.email.lower()
    user = db.query(User).filter(User.email == email, User.is_active.is_(True)).first()

    generic = ForgotPasswordResponse(
        message="Si el correo existe, se enviará un enlace de recuperación.",
    )
    if not user:
        return generic

    token_plain, token_hash = generate_reset_token()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=_settings.jwt_reset_expires_hours)
    db.add(
        PasswordResetToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
    )
    db.commit()

    if _settings.app_env != "production":
        generic.debug_token = token_plain
        generic.debug_expires_at = expires_at.isoformat()
    return generic


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)) -> None:
    token_hash = hash_reset_token(payload.token)
    record = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
        )
        .first()
    )
    if record is None or record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado",
        )

    user = db.get(User, record.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no disponible",
        )

    user.password_hash = hash_password(payload.new_password)
    user.must_change_password = False
    record.used_at = datetime.now(timezone.utc)
    db.commit()
    return None
