from importlib import import_module
from superkit.apps.config import AppConfig
from superkit.runtime.bootstrap import ensure_src_on_path


def mount_apps(app, installed_apps):
    ensure_src_on_path()

    for app_name in installed_apps:
        module = import_module(f"apps.{app_name}.app")

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

        app.include_router(app_config_cls().build_router())
