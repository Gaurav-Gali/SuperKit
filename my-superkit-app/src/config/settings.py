from superkit.settings import ProjectSettings

class Settings(ProjectSettings):
    """
    Central configuration for the SuperKit application.
    """

    # ─────────────────────────────────────────────
    # App metadata
    # ─────────────────────────────────────────────
    title: str = "my-superkit-app"
    description: str | None = None
    version: str = "0.1.0"

    # ─────────────────────────────────────────────
    # Advanced Configuration
    # ─────────────────────────────────────────────
    debug: bool = True
    lifespan: object | None = None

    # ─────────────────────────────────────────────
    # Environment (semantic only)
    # ─────────────────────────────────────────────
    environment: str = "development"

    # ─────────────────────────────────────────────
    # Server config (used by superkit CLI)
    # ─────────────────────────────────────────────
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    # ─────────────────────────────────────────────
    # Docs URL
    # ─────────────────────────────────────────────
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"

    # ─────────────────────────────────────────────
    # Environment Variables
    # ─────────────────────────────────────────────


settings = Settings()