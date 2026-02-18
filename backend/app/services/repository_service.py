from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.models.language import Language
from app.schemas.repository import RepositoryCreate
from app.utils.github import parse_github_repo

def create_repository(db: Session, payload: RepositoryCreate):
    owner, repo_name = parse_github_repo(payload.repo_url)

    language = db.query(Language).filter(
        Language.id == payload.language_id,
        Language.is_active == True
    ).first()

    if not language:
        raise ValueError("Invalid or inactive language")

    existing = db.query(Repository).filter(
        Repository.repo_url == payload.repo_url
    ).first()

    if existing:
        raise ValueError("Repository already registered")

    repo = Repository(
        name=repo_name,
        owner=owner,
        repo_url=payload.repo_url,
        language_id=payload.language_id
    )

    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo

def list_repositories(db: Session):
    return db.query(Repository).filter(Repository.is_active == True).all()
