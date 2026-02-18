from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.file_fetch_service import fetch_practice_files
from app.services.code_service import (
    fetch_practice_snippets,
    fetch_practice_snippets_by_language,
)

router = APIRouter(prefix="/code", tags=["Code Fetch"])


@router.get("/preview/{repository_id}")
def preview_code(repository_id: int, db: Session = Depends(get_db)):
    try:
        return fetch_practice_files(db, repository_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/snippets")
def fetch_code_snippets(
    language: str = Query(..., description="Language name, e.g. 'python'"),
    db: Session = Depends(get_db),
):
    try:
        return fetch_practice_snippets_by_language(db, language)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/snippets")
# def fetch_snippets_by_repo(
#     repository_id: int = Query(..., description="Repository ID to fetch snippets for"),
#     db: Session = Depends(get_db),
# ):
#     Fetch practice snippets based on repository ID
#     try:
#         return fetch_practice_snippets(db, repository_id)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))