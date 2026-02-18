from app.core.database import engine, Base
from app.models.language import Language
from app.models.repository import Repository
from app.models.snippet import CodeSnippet

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
