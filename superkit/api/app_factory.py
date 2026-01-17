from typing import Any, Callable
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.routing import BaseRoute
from starlette.responses import Response

# Application Imports
from superkit.api.application import SuperKitApp


def create_app(
    *,
    title: str = "FastAPI",
    description: str | None = None,
    version: str = "0.1.0",
    openapi_url: str | None = "/openapi.json",
    openapi_tags: list[dict[str, Any]] | None = None,
    servers: list[dict[str, Any]] | None = None,
    dependencies: list[Any] | None = None,
    default_response_class: type[Response] = JSONResponse,
    docs_url: str | None = "/docs",
    redoc_url: str | None = "/redoc",
    swagger_ui_oauth2_redirect_url: str | None = "/docs/oauth2-redirect",
    swagger_ui_init_oauth: dict[str, Any] | None = None,
    middleware: list[Middleware] | None = None,
    exception_handlers: dict[type[Exception], Callable] | None = None,
    on_startup: list[Callable] | None = None,
    on_shutdown: list[Callable] | None = None,
    lifespan: Callable | None = None,
    debug: bool = False,
    root_path: str = "",
    root_path_in_servers: bool = True,
    responses: dict[int | str, dict[str, Any]] | None = None,
    callbacks: list[BaseRoute] | None = None,
    deprecated: bool | None = None,
    include_in_schema: bool = True,
) -> SuperKitApp:
    """
    Create a SuperKit application.
    """
    return SuperKitApp(
        title=title,
        description=description,
        version=version,
        openapi_url=openapi_url,
        openapi_tags=openapi_tags,
        servers=servers,
        dependencies=dependencies,
        default_response_class=default_response_class,
        docs_url=docs_url,
        redoc_url=redoc_url,
        swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
        swagger_ui_init_oauth=swagger_ui_init_oauth,
        middleware=middleware,
        exception_handlers=exception_handlers,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        lifespan=lifespan,
        debug=debug,
        root_path=root_path,
        root_path_in_servers=root_path_in_servers,
        responses=responses,
        callbacks=callbacks,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
    )
