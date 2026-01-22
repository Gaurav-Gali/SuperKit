from importlib import import_module
from superkit.apps.config import AppConfig
from superkit.runtime.bootstrap import ensure_src_on_path
from superkit.apps.discovery import discover_apps
from superkit.apps.selection import resolve_apps


def mount_apps(
    app,
    *,
    include_all: bool = False,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
):
    ensure_src_on_path()

    discovered = discover_apps()
    app_names = resolve_apps(
        include_all=include_all,
        include=include,
        exclude=exclude,
        discovered=discovered,
    )

    # idempotency guard
    if not hasattr(app, "_mounted_apps"):
        app._mounted_apps = set()

    for app_name in app_names:
        if app_name in app._mounted_apps:
            continue

        module = import_module(f"apps.{app_name}.app")

        # ---- find AppConfig subclass ----
        app_config_cls = None
        for obj in module.__dict__.values():
            if (
                isinstance(obj, type)
                and issubclass(obj, AppConfig)
                and obj is not AppConfig
            ):
                app_config_cls = obj
                break

        if app_config_cls is None:
            raise RuntimeError(
                f"App '{app_name}' must define an AppConfig subclass"
            )

        # ---- build + mount router ----
        app_config = app_config_cls()
        app.include_router(app_config.build_router())

        app._mounted_apps.add(app_name)
