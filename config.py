from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ── Base de datos ──────────────────────────────────────────────────────────
    # Formato Azure: tu-servidor.database.windows.net
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 1433

    # ── JWT ────────────────────────────────────────────────────────────────────
    # Genera una clave segura con: openssl rand -hex 32
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── App ────────────────────────────────────────────────────────────────────
    APP_NAME: str = "Hotel API"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Instancia única de Settings durante toda la vida de la app.
    lru_cache evita releer el .env en cada request.
    Uso: from app.config import get_settings; settings = get_settings()
    """
    return Settings()