from pydantic import BaseModel, Field

class RepositoryCreate(BaseModel):
    repo_url:str = Field(..., example="https://github.com/psf/requests")
    language_id: int

class RepositoryResponse(BaseModel):
    id: int
    name: str
    owner: str
    repo_url: str
    language_id: int
    is_active: bool

    class Config:
        from_attributes = True
