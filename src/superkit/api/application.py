from fastapi import FastAPI

# Lifecycle Imports
from superkit.lifecycle.mount_apps import mount_apps as _mount_apps


class SuperKitApp(FastAPI):
    """
    SuperKit application instance.
    """

    def __init__(self, *, environment: str = "development", **kwargs):
        super().__init__(**kwargs)

        # Metadata only
        self.environment = environment

        # Internal state
        self.state.installed_apps = None
        self.state.settings = None
        self.state.security = None

        # Internal mount tracking (idempotency)
        self._mounted_apps = set()

    # Lifecycle API (Chaining)
    def mount_apps(
        self,
        *,
        include_all: bool = False,
        include: list[str] | None = None,
        exclude: list[str] | None = None,
    ):
        if self.state.installed_apps is not None:
            raise RuntimeError(
                "mount_apps() can only be called once per application instance."
            )

        # Delegate to framework lifecycle
        mounted_apps = _mount_apps(
            self,
            include_all=include_all,
            include=include,
            exclude=exclude,
        )

        # Persist resolved apps (not raw input)
        self.state.installed_apps = mounted_apps

        return self

    def apply_security(self):
        return self
