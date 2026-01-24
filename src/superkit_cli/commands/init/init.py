import typer
from pathlib import Path
from importlib.resources import files

from superkit_cli.ui.setup_wizard import setup_wizard
from superkit_cli.scaffold.renderer import render_template_dir

init_app = typer.Typer()

@init_app.command('init')
def init():
    data = setup_wizard()

    if data is None:
        raise typer.Exit(1)

    project_name = data["project_name"]
    target_dir = (
        Path.cwd()
        if project_name == "."
        else Path.cwd() / project_name
    )

    if target_dir.exists() and any(target_dir.iterdir()):
        typer.secho(
            "Error: Target directory is not empty.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)

    template_root = files("superkit_cli.templates") / "default"

    render_template_dir(
        template_dir=template_root,
        target_dir=target_dir,
        context={
            "project_name": (
                target_dir.name
                if project_name == "."
                else project_name
            ),
            "app_instance": data["app_instance"],
            "environment": data["environment"],
        },
    )

    # Status
    typer.secho("\n● SuperKit project initialized successfully!\n", fg=typer.colors.GREEN)
    typer.echo("Next steps:")
    if project_name != ".":
        typer.echo(f"  " + typer.style("→", fg=typer.colors.CYAN) + f" cd {target_dir.name}")

    typer.echo(f"  " + typer.style("→", fg=typer.colors.CYAN) + f" superkit run {data['app_instance']}\n")