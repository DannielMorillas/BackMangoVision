from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Disease
from app.schemas.disease import DiseaseRead

router = APIRouter(prefix="/api/diseases", tags=["diseases"])


@router.get("", response_model=list[DiseaseRead])
def list_diseases(db: Session = Depends(get_db)) -> list[Disease]:
    return db.query(Disease).order_by(Disease.id).all()
