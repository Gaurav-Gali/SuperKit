import typer
import os

from superkit_cli.bootstrap_loader import bootstrap_loader

from superkit.runtime.registry import runtime
from superkit_cli.ui.runtime.server_info import server_info

run_app = typer.Typer(help="Run a SuperKit / FastAPI application")


@run_app.command("run")
def run(
    instance: str = typer.Argument(
        ...,
        help="App instance name defined in main.py (e.g. app, dev, prod)",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        help="Override host from settings",
    ),
    port: int | None = typer.Option(
        None,
        "--port",
        help="Override port from settings",
    ),
    reload: bool | None = typer.Option(
        None,
        "--reload/--no-reload",
        help="Override reload from settings",
    ),
):
    # Bootstrap Loader
    bootstrap_loader()


    # ─────────────────────────────────────────────
    # Resolve server configuration
    # ─────────────────────────────────────────────
    server = runtime.server
    settings = runtime.settings

    resolved_host = host if host is not None else server["host"]
    resolved_port = port if port is not None else server["port"]
    resolved_reload = reload if reload is not None else server["reload"]
    environment = server.get("environment", "development")

    # ─────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────
    server_info(
        app_name=settings.get("title", "SuperKit App"),
        instance=instance,
        host=resolved_host,
        port=resolved_port,
        reload=resolved_reload,
        environment=environment,
        docs_enabled=settings.get("docs_url") is not None,
    )

    # ─────────────────────────────────────────────
    # Run uvicorn
    # ─────────────────────────────────────────────
    cmd = [
        "uvicorn",
        f"main:{instance}",
        "--app-dir", "src",
        "--host", resolved_host,
        "--port", str(resolved_port),
    ]

    if resolved_reload:
        cmd.append("--reload")

    os.execvp(cmd[0], cmd)
