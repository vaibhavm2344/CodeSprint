from pydantic import BaseModel, Field

class LanguageBase(BaseModel):
    name: str = Field(..., example="python")
    display_name: str = Field(..., example="Python")

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
