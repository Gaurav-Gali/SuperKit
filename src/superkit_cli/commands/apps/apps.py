import typer

from superkit_cli.commands.apps.init import init_app

apps_app = typer.Typer()

# Commands
apps_app.command('init')(init_app)


