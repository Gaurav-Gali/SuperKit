import typer

# Commands Import
from superkit_cli.commands.run.run import run_app
from superkit_cli.commands.init.init import init_app

app = typer.Typer(
    help="SuperKit CLI"
)

# Registering Commands
app.add_typer(run_app)
app.add_typer(init_app)

def main():
    app()
