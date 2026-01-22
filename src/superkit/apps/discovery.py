import pkgutil
from importlib import import_module


def discover_apps() -> set[str]:
    """
    Discover valid apps under the `apps` package.
    """
    apps = set()

    try:
        apps_pkg = import_module("apps")
    except ModuleNotFoundError:
        return apps

    for _, name, is_pkg in pkgutil.iter_modules(apps_pkg.__path__):
        if not is_pkg:
            continue

        try:
            import_module(f"apps.{name}.app")
        except ModuleNotFoundError:
            continue

        apps.add(name)

    return apps
