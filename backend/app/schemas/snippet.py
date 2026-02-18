from pydantic import BaseModel


class CodeSnippetOut(BaseModel):
    id: int
    repository_id: int
    source_url: str
    code: str

    class Config:
        orm_mode = True
