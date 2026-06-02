from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.db import get_db
from app.core.security import hash_password
from app.models import Image, MLModel, Prediction, User
from app.schemas.system import ActivityLogEntry, MLModelRead, MLModelStatusUpdate
from app.schemas.user import UserCreate, UserRead, UserStatusUpdate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[User]:
    return db.query(User).order_by(User.id).all()


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> User:
    email = payload.email.lower()
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo",
        )

    user = User(
        email=email,
        password_hash=hash_password(payload.temp_password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        role=payload.role,
        is_active=True,
        must_change_password=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/status", response_model=UserRead)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> User:
    if user_id == admin.id and not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrador no puede desactivarse a sí mismo",
        )
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user


# --- Gestión de modelos IA (EN-010) ---

@router.get("/models", response_model=list[MLModelRead])
def list_models(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[MLModel]:
    return db.query(MLModel).order_by(MLModel.created_at.desc()).all()


@router.patch("/models/{model_id}", response_model=MLModelRead)
def set_model_status(
    model_id: int,
    payload: MLModelStatusUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> MLModel:
    model = db.get(MLModel, model_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modelo no encontrado")
    # Activar un modelo desactiva el resto (un único modelo activo a la vez).
    if payload.is_active:
        for other in db.query(MLModel).filter(MLModel.is_active.is_(True), MLModel.id != model_id):
            other.is_active = False
    model.is_active = payload.is_active
    db.commit()
    db.refresh(model)
    return model


# --- Logs de actividad (EN-010) ---

@router.get("/logs", response_model=list[ActivityLogEntry])
def activity_logs(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ActivityLogEntry]:
    """Feed de actividad derivado de las tablas existentes (sin tabla de logs dedicada).

    Combina altas de usuarios, logins, subidas de imágenes y predicciones, ordenado por fecha.
    """
    entries: list[ActivityLogEntry] = []

    for u in db.query(User).all():
        entries.append(
            ActivityLogEntry(
                timestamp=u.created_at,
                tipo="alta_usuario",
                descripcion=f"Alta de usuario {u.email} ({u.role.value})",
                usuario=u.email,
            )
        )
        if u.last_login_at is not None:
            entries.append(
                ActivityLogEntry(
                    timestamp=u.last_login_at,
                    tipo="login",
                    descripcion=f"Inicio de sesión de {u.email}",
                    usuario=u.email,
                )
            )

    users_by_id = {u.id: u for u in db.query(User).all()}
    for img in db.query(Image).order_by(Image.uploaded_at.desc()).limit(limit).all():
        owner = users_by_id.get(img.user_id)
        entries.append(
            ActivityLogEntry(
                timestamp=img.uploaded_at,
                tipo="upload",
                descripcion=f"Imagen subida: {img.original_filename}",
                usuario=owner.email if owner else None,
            )
        )

    for image_id, created_at, n in (
        db.query(Prediction.image_id, Prediction.created_at, Prediction.id)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
        .all()
    ):
        entries.append(
            ActivityLogEntry(
                timestamp=created_at,
                tipo="prediccion",
                descripcion=f"Diagnóstico generado para imagen #{image_id}",
                usuario=None,
            )
        )

    entries.sort(key=lambda e: e.timestamp, reverse=True)
    return entries[:limit]
