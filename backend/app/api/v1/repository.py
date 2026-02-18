from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.repository_service import create_repository, list_repositories

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.post("/", response_model=RepositoryResponse)
def add_repository(payload: RepositoryCreate, db: Session = Depends(get_db)):
    try:
        return create_repository(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[RepositoryResponse])
def get_repositories(db: Session = Depends(get_db)):
    return list_repositories(db)
