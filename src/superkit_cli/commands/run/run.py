import typer
import uvicorn
import importlib.util
from pathlib import Path
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

from superkit_cli.bootstrap_loader import bootstrap_loader
from superkit.runtime.registry import runtime
from superkit_cli.ui.runtime.server_info import server_info

run_app = typer.Typer()
console = Console()


def show_error(message: str):
    """Display error message in a rich panel"""

    error_text = Text(message, style="red")
    panel = Panel(
        error_text,
        title="Error",
        border_style="red",
        title_align="left",
        padding=(1, 2),
    )
    console.print(panel)


def validate_app_instance(instance: str) -> bool:
    """
    Validate that the apps instance exists and is a FastAPI apps.
    Returns True if valid, False otherwise.
    """
    main_path = Path("src/main.py")

    if not main_path.exists():
        show_error("src/main.py not found")
        return False

    try:
        # Load the module to validate
        spec = importlib.util.spec_from_file_location("main", main_path)
        if spec is None or spec.loader is None:
            show_error("Could not load main.py")
            return False

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    except Exception as e:
        show_error(f"Error importing main.py: {e}")
        return False

    if not hasattr(module, instance):
        show_error(f"App instance '{instance}' not found in main.py")
        return False

    app = getattr(module, instance)

    # Check if it's a FastAPI instance
    from fastapi import FastAPI
    if not isinstance(app, FastAPI):
        show_error(f"'{instance}' exists but is not a FastAPI apps")
        return False

    return True


@run_app.command("run")
def run(
        instance: str = typer.Argument(
            ...,
            help="App instance name defined in main.py (e.g. apps, dev, prod)",
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
    # Validate apps instance before starting server
    # ─────────────────────────────────────────────
    if not validate_app_instance(instance):
        raise typer.Exit(1)

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
    # Configure uvicorn to show errors but hide logs
    # ─────────────────────────────────────────────
    log_config = uvicorn.config.LOGGING_CONFIG
    # Keep error logging enabled
    log_config["loggers"]["uvicorn.error"]["level"] = "ERROR"
    # Disable access logging
    log_config["loggers"]["uvicorn.access"]["handlers"] = []

    # ─────────────────────────────────────────────
    # Run uvicorn
    # ─────────────────────────────────────────────
    uvicorn.run(
        f"main:{instance}",
        app_dir="src",
        host=resolved_host,
        port=resolved_port,
        reload=resolved_reload,
        log_config=log_config,
    )