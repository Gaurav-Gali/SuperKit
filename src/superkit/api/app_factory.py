from superkit.api.application import SuperKitApp
from superkit.runtime.registry import runtime
from superkit.logging import setup_logging

from superkit.runtime.bootstrap import ensure_src_on_path

def create_app(
    *,
    settings=None,
    environment: str = "development",
    **kwargs,
) -> SuperKitApp:
    # Source on path
    ensure_src_on_path()

    # Initializing Logging
    setup_logging()


    fastapi_kwargs = {}
    server_config = {}

    if settings is not None:
        # FastAPI kwargs
        for key in (
            "title",
            "description",
            "version",
            "debug",
            "docs_url",
            "redoc_url",
            "openapi_url",
            "lifespan",
        ):
            value = getattr(settings, key, None)
            if value is not None:
                fastapi_kwargs[key] = value

        if hasattr(settings, "fastapi_kwargs"):
            fastapi_kwargs.update(settings.fastapi_kwargs)

        # Server config (NOT passed to FastAPI)
        server_config = {
            "host": settings.host,
            "port": settings.port,
            "reload": settings.reload,
            "environment": environment,
        }

    fastapi_kwargs.update(kwargs)

    app = SuperKitApp(
        environment=environment,
        **fastapi_kwargs,
    )

    # Initialize runtime once
    if settings is not None and not runtime.is_initialized():
        runtime.initialize(
            settings=fastapi_kwargs,
            server=server_config,
        )

    return app
