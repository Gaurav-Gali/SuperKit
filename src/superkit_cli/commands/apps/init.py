import typer
import re
from pathlib import Path
from importlib.resources import files

from superkit_cli.scaffold.renderer import render_template_dir

apps_init = typer.Typer()

VALID_APP_NAME = re.compile(r"^[a-z_][a-z0-9_]*$")


@apps_init.command("init")
def init_app(app_name: str):
    # ---- validate app name ----
    if not VALID_APP_NAME.match(app_name):
        typer.secho(
            f"Invalid app name '{app_name}'. "
            "Use lowercase letters, numbers, and underscores only.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # ---- locate project root (src/) ----
    project_root = Path.cwd()
    src_dir = project_root / "src"
    apps_dir = src_dir / "apps"

    if not src_dir.exists():
        typer.secho(
            "Error: Not a SuperKit project (src/ not found).",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # ---- ensure apps/ exists ----
    apps_dir.mkdir(parents=True, exist_ok=True)

    target_app_dir = apps_dir / app_name

    # ---- prevent overwrite ----
    if target_app_dir.exists():
        typer.secho(
            f"Error: App '{app_name}' already exists.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # ---- render templates ----
    template_root = files("superkit_cli.templates") / "app"

    render_template_dir(
        template_dir=template_root,
        target_dir=target_app_dir,
        context={
            "app_name": app_name,
            "class_name": app_name.capitalize(),
        },
    )

    # ---- rename controller file ----
    default_controller = target_app_dir / "controllers" / "controller.py"
    if default_controller.exists():
        default_controller.rename(
            target_app_dir / "controllers" / f"{app_name}.py"
        )

    # ---- success message ----
    typer.secho(f"\n● App '{app_name}' created successfully!\n", fg=typer.colors.GREEN)

    typer.echo("Next steps:")
    typer.echo(
        "  " + typer.style("→", fg=typer.colors.CYAN)
        + f" mount it inside mount_apps(...) in main.py"
    )
    typer.echo(
        "  " + typer.style("→", fg=typer.colors.CYAN)
        + f" path: src/apps/{app_name}\n"
    )

