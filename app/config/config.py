import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    sqlalchemy_database_url: str = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    secret_key: str = os.getenv("SECRET_KEY", "supersecret")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI", "")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:8080")

settings = Settings()
