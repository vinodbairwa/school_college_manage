from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load backend/.env regardless of process cwd
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "EduNest SaaS"
    secret_key: str = "dev-secret-change-in-production-edu-nest-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    # Default local SQLite; production / docker use MySQL, e.g.
    # mysql+pymysql://edunest:edunest@127.0.0.1:3306/edunest
    database_url: str = "sqlite:///./school_saas.db"
    upload_dir: str = "uploads"
    base_domain: str = "localhost"
    max_upload_mb: int = 5
    # Comma-separated origins for Next.js website + React panel
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"
    website_url: str = "http://localhost:3000"
    panel_url: str = "http://localhost:5173"

    @property
    def upload_path(self) -> Path:
        # Resolve relative to backend/ package root
        base = Path(__file__).resolve().parents[1]
        path = Path(self.upload_dir)
        if not path.is_absolute():
            path = base / path
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
