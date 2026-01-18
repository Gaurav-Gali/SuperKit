import typer
from pathlib import Path
from importlib.resources import files

from superkit_cli.ui.setup_wizard import setup_wizard

init_app = typer.Typer(help="Initialize a new SuperKit project")

@init_app.command('init')
def init():
    data = setup_wizard()

    print(data)