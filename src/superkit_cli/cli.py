import typer

# Commands Import
from superkit_cli.commands.run.run import run_app

app = typer.Typer(
    help="SuperKit CLI"
)

# Registering Commands
app.add_typer(run_app)

def main():
    app()
