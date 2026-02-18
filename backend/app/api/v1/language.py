from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.language import LanguageCreate, LanguageResponse
from app.services.language_service import create_language, get_languages

router = APIRouter(prefix="/languages", tags=["Languages"])

@router.post("/", response_model=LanguageResponse)
def add_language(payload: LanguageCreate, db: Session = Depends(get_db)):
    try:
        return create_language(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[LanguageResponse])
def list_languages(db: Session = Depends(get_db)):
    return get_languages(db)
