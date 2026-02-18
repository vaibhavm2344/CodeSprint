import random
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.language import Language
from app.models.snippet import CodeSnippet
from app.utils.download_url import fetch_download_urls
from app.utils.fetch_code import fetch_code_from_urls
from app.utils.github_fetch import fetch_repo_tree
from app.utils.file_filter import filter_code_files


def fetch_practice_snippets(db: Session, repository_id: int):
    existing = db.query(CodeSnippet).filter(
        CodeSnippet.repository_id == repository_id
    ).all()

    if existing:
        snippet = random.choice(existing)
        return {
            "source": "db",
            "code": snippet.code
        }

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

    from app.utils.language_extensions import LANGUAGE_ALIASES
    canonical = LANGUAGE_ALIASES.get(language.name.lower(), language.name.lower())
    tree, branch = fetch_repo_tree(repo.owner, repo.name)
    files = filter_code_files(tree, canonical)
    download_urls = fetch_download_urls(repo.owner, repo.name, files, branch=branch)
    raw_code = fetch_code_from_urls(download_urls, language=canonical)

    if not raw_code:
        raise ValueError("No valid code snippets found")

    snippets = []
    for item in raw_code:
        snippet = CodeSnippet(
            repository_id=repository_id,
            source_url=item["url"],
            code=item["code"]
        )
        snippets.append(snippet)

    db.add_all(snippets)
    db.commit()

    selected = random.choice(snippets)

    return {
        "source": "github",
        "code": selected.code
    }


def fetch_practice_snippets_by_language(db: Session, language_name: str):
    from app.utils.language_extensions import LANGUAGE_ALIASES

    normalized = LANGUAGE_ALIASES.get(language_name.lower(), language_name.lower())
    languages = db.query(Language).filter(Language.is_active == True).all()
    language = None
    for lang in languages:
        canonical = LANGUAGE_ALIASES.get(lang.name.lower(), lang.name.lower())
        if canonical == normalized:
            language = lang
            break
    if not language:
        raise ValueError("Language not found")

    repo = (
        db.query(Repository)
        .filter(
            Repository.language_id == language.id,
            Repository.is_active == True,
        )
        .order_by(func.random())
        .first()
    )
    if not repo:
        raise ValueError("No repositories configured for this language")

    repository_id = repo.id

    existing = db.query(CodeSnippet).filter(
        CodeSnippet.repository_id == repository_id
    ).all()

    if existing:
        snippet = random.choice(existing)
        return {
            "source": "db",
            "code": snippet.code
        }

    tree, branch = fetch_repo_tree(repo.owner, repo.name)
    files = filter_code_files(tree, normalized)
    download_urls = fetch_download_urls(repo.owner, repo.name, files, branch=branch)
    raw_code = fetch_code_from_urls(download_urls, language=normalized)

    if not raw_code:
        raise ValueError("No valid code snippets found")

    snippets = []
    for item in raw_code:
        snippet = CodeSnippet(
            repository_id=repository_id,
            source_url=item["url"],
            code=item["code"]
        )
        snippets.append(snippet)

    db.add_all(snippets)
    db.commit()

    selected = random.choice(snippets)

    return {
        "source": "github",
        "code": selected.code
    }
