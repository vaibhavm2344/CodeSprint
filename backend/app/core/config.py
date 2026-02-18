import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "CodeSprint")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

settings = Settings()
