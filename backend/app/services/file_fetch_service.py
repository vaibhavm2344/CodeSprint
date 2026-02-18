from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.language import Language
from app.utils.github_fetch import fetch_repo_tree
from app.utils.file_filter import filter_code_files

def fetch_practice_files(db: Session, repository_id: int):
    repo = db.query(Repository).filter(
        Repository.id == repository_id,
        Repository.is_active == True
    ).first()

    if not repo:
        raise ValueError("Repository not found")

    language = db.query(Language).filter(
        Language.id == repo.language_id,
        Language.is_active == True
    ).first()

    if not language:
        raise ValueError("Language not found")

    tree, _ = fetch_repo_tree(repo.owner, repo.name)
    files = filter_code_files(tree, language.name)

    return {
        "repository": repo.repo_url,
        "language": language.name,
        "total_files": len(files),
        "files": files[:50]  # limit for now
    }
