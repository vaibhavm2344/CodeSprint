from sqlalchemy.orm import Session
from app.models.language import Language
from app.schemas.language import LanguageCreate

def create_language(db: Session, language: LanguageCreate):
    existing = db.query(Language).filter(Language.name == language.name).first()
    if existing:
        raise ValueError("Language already exists")

    lang = Language(
        name=language.name.lower(),
        display_name=language.display_name
    )

    db.add(lang)
    db.commit()
    db.refresh(lang)
    return lang

def get_languages(db: Session, active_only: bool = True):
    query = db.query(Language)
    if active_only:
        query = query.filter(Language.is_active == True)
    return query.all()
