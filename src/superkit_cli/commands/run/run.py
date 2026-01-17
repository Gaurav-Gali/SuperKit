import typer
import os
from pathlib import Path

from superkit_cli.ui.runtime.server_info import server_info

run_app = typer.Typer(help="Run a SuperKit / FastAPI application")


@run_app.command("run")
def run(
    instance: str = typer.Argument(
        ...,
        help="App instance name defined in main.py (e.g. app, dev, prod)",
    ),
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(True, "--reload/--no-reload"),
):
    """
    Run an app instance from main.py using uvicorn.
    """

    cwd = Path.cwd()
    main_file = cwd / "main.py"

    if not main_file.exists():
        typer.secho(
            "Error: main.py not found in the current directory.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    cmd = [
        "uvicorn",
        f"main:{instance}",
        "--host", host,
        "--port", str(port),
    ]

    if reload:
        cmd.append("--reload")

    server_info(
        app_name="MyApp",
        instance="app",
        host=host,
        port=port,
        reload=reload,
        environment="development",
        docs_enabled=True,
    )

    os.execvp(cmd[0], cmd)
