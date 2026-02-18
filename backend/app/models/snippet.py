from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True)

    repository_id = Column(Integer, ForeignKey("repositories.id"), index=True)
    # language_id = Column(Integer, ForeignKey("languages.id"), index=True)

    source_url = Column(Text, nullable=False)
    code = Column(Text, nullable=False)

    lines_count = Column(Integer)
    snippet_hash = Column(String(64), unique=True, index=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    repository = relationship("Repository", back_populates="snippets")
    # language = relationship("Language", back_populates="snippets")
