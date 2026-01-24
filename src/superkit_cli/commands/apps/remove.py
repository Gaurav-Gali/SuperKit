import shutil
import typer
from pathlib import Path

from superkit_cli.utils.project import find_project_root


def remove_app(app_name: str):
    try:
        project_root = find_project_root()
    except RuntimeError as e:
        print(f"\n\033[91mError: {e}\033[0m\n")
        return

    app_dir = project_root / "src" / "apps" / app_name

    if not app_dir.exists():
        print(f"\n\033[91mError: App '{app_name}' does not exist\033[0m\n")
        return

    print(f"\n\033[93m⚠  Warning: This will permanently delete the app '{app_name}'\033[0m")
    print(f"   \033[90mPath: apps/{app_name}\033[0m\n")

    confirm = typer.confirm(
        "   Are you sure you want to continue?",
        default=False,
    )

    if not confirm:
        print(f"\n\033[90mOperation cancelled\033[0m\n")
        return

    shutil.rmtree(app_dir)

    print(f"\n\033[92m● App '{app_name}' has been removed successfully\033[0m\n")