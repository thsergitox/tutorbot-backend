import os
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "TutorBot"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DB_URL = os.getenv("DB_URL")
    port = int(os.getenv("PORT", 8000))


settings = Settings()
