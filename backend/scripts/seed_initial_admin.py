"""Crea o reactiva el primer usuario administrador del sistema.

Idempotente: si el admin ya existe, no falla — solo asegura que esté activo.
Ideal para ejecutar una vez tras `alembic upgrade head` para poder loguearse.

Uso:
    python scripts/seed_initial_admin.py
    python scripts/seed_initial_admin.py --email admin@araexport.com.pe --password ClaveTemporal

Variables de entorno (toman precedencia sobre los defaults si no se pasan flags):
    INITIAL_ADMIN_EMAIL
    INITIAL_ADMIN_PASSWORD
"""
from __future__ import annotations

import argparse
import os
import sys

from app.core.db import SessionLocal
from app.core.security import hash_password
from app.models import User, UserRole


DEFAULT_EMAIL = "admin@araexport.example"
DEFAULT_PASSWORD = "CambiameYa#2026"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed inicial del admin de MangoVision.")
    p.add_argument(
        "--email",
        default=os.getenv("INITIAL_ADMIN_EMAIL", DEFAULT_EMAIL),
        help="Email del admin (default: %(default)s).",
    )
    p.add_argument(
        "--password",
        default=os.getenv("INITIAL_ADMIN_PASSWORD", DEFAULT_PASSWORD),
        help="Contraseña temporal del admin (default: oculto).",
    )
    p.add_argument(
        "--first-name",
        default="Administrador",
        help="Nombre (default: %(default)s).",
    )
    p.add_argument(
        "--last-name",
        default="MangoVision",
        help="Apellido (default: %(default)s).",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    email = args.email.lower().strip()

    with SessionLocal() as session:
        existing = session.query(User).filter(User.email == email).first()
        if existing:
            if not existing.is_active:
                existing.is_active = True
                session.commit()
                print(f"Reactivado admin existente: {email}")
            elif existing.role != UserRole.ADMIN:
                print(
                    f"[!] El usuario {email} existe pero no es admin (role={existing.role.value}). "
                    "No se modifica.",
                    file=sys.stderr,
                )
                return 1
            else:
                print(f"Admin ya existe y está activo: {email} (sin cambios)")
            return 0

        admin = User(
            email=email,
            password_hash=hash_password(args.password),
            first_name=args.first_name,
            last_name=args.last_name,
            role=UserRole.ADMIN,
            is_active=True,
            must_change_password=True,
        )
        session.add(admin)
        session.commit()
        print(f"Admin creado: {email}")
        print(f"Contraseña temporal: {args.password}")
        print("Recuerda cambiarla en el primer login.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
