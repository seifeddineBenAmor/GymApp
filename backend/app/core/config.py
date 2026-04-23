from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "UrbanGym"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    UPLOAD_DIR: str = "uploads"
    VIDEO_DIR: str = "videos"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"        # ignore vars in .env that aren't in Settings


settings = Settings()