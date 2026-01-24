from pathlib import Path
from superkit.apps.config import AppConfig
from superkit_cli.utils.project import find_project_root


def info_app(app_name: str):
    from superkit.apps.discovery import get_apps_context
    import sys

    apps_path, search_root = get_apps_context()

    if not apps_path or not search_root:
        print(f"\n\033[91mError: Not inside a SuperKit project (apps/ folder not found)\033[0m\n")
        return

    app_dir = apps_path / app_name
    if not app_dir.exists():
        print(f"\n\033[91mError: App '{app_name}' not found\033[0m\n")
        return

    # Ensure search_root is in sys.path
    search_root_str = str(search_root)
    if search_root_str not in sys.path:
        sys.path.insert(0, search_root_str)

    # ---- load AppConfig ----
    try:
        module = __import__(f"apps.{app_name}.app", fromlist=["*"])
    except Exception as e:
        print(f"\n\033[91mError: Failed to import app '{app_name}': {e}\033[0m\n")
        return

    app_config = None
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, AppConfig) and obj is not AppConfig:
            app_config = obj()
            break

    if app_config is None:
        print(f"\n\033[91mError: No AppConfig found in apps.{app_name}.app\033[0m\n")
        return

    # ---- AppConfig summary ----
    relative_path = f"apps/{app_name}"

    print(f"\n\033[1m\033[96mApp: {app_config.name}\033[0m\n")
    print(f"  \033[90mPath:      \033[0m {relative_path}")
    print(f"  \033[90mURL Prefix:\033[0m {app_config.url_prefix}")
    print(f"  \033[90mTags:      \033[0m {', '.join(app_config.tags) if app_config.tags else 'None'}")

    # ---- Routes ----
    try:
        router = app_config.build_router()
    except Exception as e:
        print(f"\n\033[91mError: Failed to build router: {e}\033[0m\n")
        return

    routes = []
    for route in router.routes:
        methods = getattr(route, "methods", None)
        if not methods:
            continue
        for method in methods:
            routes.append((method, route.path))

    if routes:
        print(f"\n\033[1m\033[96mRoutes:\033[0m\n")
        for method, path in routes:
            method_color = "\033[92m" if method == "GET" else "\033[93m" if method == "POST" else "\033[94m"
            print(f"  \033[1m\033[92m→\033[0m  {method_color}{method:<6}\033[0m {path}")
    else:
        print(f"\n\033[93mNo routes found\033[0m")

    # ---- Controllers tree ----
    controllers_dir = app_dir / "controllers"

    if controllers_dir.exists():
        controllers = []
        for path in sorted(controllers_dir.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            controllers.append(path.relative_to(controllers_dir))

        if controllers:
            print(f"\n\033[1m\033[96mControllers:\033[0m\n")

            # Build tree structure
            tree = {}
            for controller in controllers:
                parts = controller.parts
                current = tree
                for part in parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

            def print_tree(node, prefix="", is_root=True):
                items = sorted(node.items())
                for i, (name, children) in enumerate(items):
                    is_last_item = i == len(items) - 1

                    if is_root:
                        connector = ""
                        print(f"  \033[1m\033[92m→\033[0m  {name}")
                    else:
                        connector = "└── " if is_last_item else "├── "
                        print(f"  {prefix}{connector}{name}")

                    if children:
                        if is_root:
                            extension = ""
                        else:
                            extension = "    " if is_last_item else "│   "
                        print_tree(children, prefix + extension, is_root=False)

            print_tree(tree)

    print()