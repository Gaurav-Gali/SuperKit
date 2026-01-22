import importlib
import pkgutil


def import_controllers(
    package_name: str,
    package_path,
    *,
    recursive: bool,
) -> None:
    """
    Import controller modules in a package.

    If recursive=True, subpackages are imported as well.
    """
    for _, name, is_pkg in pkgutil.iter_modules(package_path):
        if name.startswith("_"):
            continue

        module = importlib.import_module(f"{package_name}.{name}")

        if is_pkg and recursive:
            import_controllers(
                module.__name__,
                module.__path__,
                recursive=True,
            )
