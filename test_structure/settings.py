from typing import Callable, Optional, Any, Dict
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Project settings for SuperKit.
    """

    # ─────────────────────────────────────────────
    # FastAPI metadata (first-class)
    # ─────────────────────────────────────────────
    title: str = "SuperKit App (Testing)"
    description: Optional[str] = None
    version: str = "0.1.0"

    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
    openapi_url: Optional[str] = "/openapi.json"

    debug: bool = False
    lifespan: Optional[Callable[..., Any]] = None

    # ─────────────────────────────────────────────
    # FastAPI pass-through kwargs (explicit escape hatch)
    # ─────────────────────────────────────────────
    fastapi_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional FastAPI constructor keyword arguments",
    )

    # ─────────────────────────────────────────────
    # Server / CLI
    # ─────────────────────────────────────────────
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
