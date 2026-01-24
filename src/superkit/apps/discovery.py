import sys
from pathlib import Path
from importlib import import_module


def get_apps_context() -> tuple[Path | None, Path | None]:
    """
    Search for the apps directory and return (apps_path, search_root).
    """
    current = Path.cwd()
    apps_path = None
    search_root = None
    
    for parent in [current, *current.parents]:
        # Case 1: root/apps/
        if (parent / "apps").exists() and (parent / "apps").is_dir():
            apps_path = parent / "apps"
            search_root = parent
            break
        # Case 2: root/src/apps/
        if (parent / "src" / "apps").exists() and (parent / "src" / "apps").is_dir():
            apps_path = parent / "src" / "apps"
            search_root = parent / "src"
            break
            
    return apps_path, search_root


def discover_apps() -> set[str]:
    """
    Discover valid apps under the `apps` package by searching for the 
    `apps` directory in the current directory or upwards.
    """
    apps = set()
    apps_path, search_root = get_apps_context()

    if not apps_path or not search_root:
        return apps


    # Ensure search_root is in sys.path so 'import apps' works
    search_root_str = str(search_root)
    if search_root_str not in sys.path:
        sys.path.insert(0, search_root_str)

    from superkit.apps.config import AppConfig
    import importlib.util

    for item in apps_path.iterdir():
        if item.is_dir() and (item / "__init__.py").exists():
            app_name = item.name
            app_module_path = item / "app.py"
            
            if app_module_path.exists():
                try:
                    # Import the module to check for AppConfig
                    module_name = f"apps.{app_name}.app"
                    spec = importlib.util.spec_from_file_location(module_name, app_module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Check if any class in the module is a subclass of AppConfig
                        for obj in module.__dict__.values():
                            if (
                                isinstance(obj, type)
                                and issubclass(obj, AppConfig)
                                and obj is not AppConfig
                            ):
                                apps.add(app_name)
                                break
                except Exception:
                    # If import fails or validation fails, skip this app
                    continue

    return apps



