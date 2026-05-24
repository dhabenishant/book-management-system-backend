from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "book_management"
    jwt_secret: str = "your-super-secret-key-change-this"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
