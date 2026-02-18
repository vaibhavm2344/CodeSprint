from fastapi import APIRouter
from app.api.v1 import health, language, repository, code

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(language.router)
api_router.include_router(repository.router)
api_router.include_router(code.router)