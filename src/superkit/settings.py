from pydantic_settings import BaseSettings
from pydantic import Field


class ProjectSettings(BaseSettings):
    """
    Base settings class for SuperKit projects.

    Users should subclass this and override only what they need.
    """

    # ─────────────────────────────────────────────
    # FastAPI metadata
    # ─────────────────────────────────────────────
    title: str = "SuperKit App"
    description: str | None = None
    version: str = "0.1.0"

    # ─────────────────────────────────────────────
    # Advanced FastAPI configuration
    # ─────────────────────────────────────────────
    debug: bool = False
    lifespan:object | None = None

    # Escape hatch for unsupported FastAPI kwargs
    fastapi_kwargs: dict = Field(default_factory=dict)

    # ─────────────────────────────────────────────
    # Environment (semantic only)
    # ─────────────────────────────────────────────
    environment: str = "development"

    # ─────────────────────────────────────────────
    # Server / CLI configuration
    # ─────────────────────────────────────────────
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    # ─────────────────────────────────────────────
    # Docs URLs
    # ─────────────────────────────────────────────
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"

    class Config:
        env_prefix = ""
        env_file = ".env"
        case_sensitive = False
