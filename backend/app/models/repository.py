from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    owner = Column(String(100), nullable=False)
    repo_url = Column(String(255), unique=True, nullable=False)

    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    language = relationship("Language", back_populates="repositories")

    snippets = relationship(
        "CodeSnippet",
        back_populates="repository",
        cascade="all, delete-orphan"
    )
