import typer

# Commands Import
from superkit_cli.commands.run.run import run
from superkit_cli.commands.init.init import init

# Subgroups Import
from superkit_cli.commands.apps.apps import apps_app

# Typer Instance
app = typer.Typer(
    help="SuperKit CLI"
)

# Registering Commands
app.command('init', help="Initializes SuperKit CLI")(init)
app.command('run', help="Runs SuperKit Application")(run)

# Subgroups
app.add_typer(
    apps_app,
    name="apps",
    help="Manages SuperKit Apps",
)

def main():
    app()
