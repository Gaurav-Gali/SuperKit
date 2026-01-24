import typer

from superkit_cli.commands.apps.init import init_app
from superkit_cli.commands.apps.list import list_apps
from superkit_cli.commands.apps.info import info_app
from superkit_cli.commands.apps.remove import remove_app
from superkit_cli.commands.apps.doctor import doctor_apps

apps_app = typer.Typer()

# Commands
apps_app.command('init', help="Initializes superkit apps, app Structure")(init_app)
apps_app.command('list', help="Lists superkit apps in the app Structure")(list_apps)
apps_app.command('info', help="Provides detailed info about the chosen app")(info_app)
apps_app.command('remove', help="Provides detailed info about the chosen app")(remove_app)
apps_app.command('doctor', help="Provides detailed info about the chosen app")(doctor_apps)

