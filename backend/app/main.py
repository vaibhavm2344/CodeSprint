from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned API
app.include_router(api_router, prefix="/api/v1")

# Convenience alias so frontend can call `/api/...` as specified
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to CodeSprint 🚀"}
