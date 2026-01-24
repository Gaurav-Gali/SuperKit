from superkit.apps.discovery import discover_apps
from superkit_cli.utils.project import find_project_root

def list_apps():
    try:
        find_project_root()
    except RuntimeError as e:
        print(f"\033[91mError: {e}\033[0m")
        return

    apps = sorted(discover_apps())

    if not apps:
        print("\n\033[93mNo apps found\033[0m\n")
        return

    print("\n\033[1m\033[96mApps:\033[0m\n")
    for app in apps:
        print(f"  \033[1m\033[92m→\033[0m  {app}")
    print()