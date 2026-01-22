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


    # Lifecycle API (Chaining)
    def mount_apps(self, installed_apps):
        if self.state.installed_apps is not None:
            raise RuntimeError(
                "mount_apps() can only be called once per application instance."
            )

        _mount_apps(self, installed_apps)
        self.state.installed_apps = list(installed_apps)

        return self

    def apply_security(self):
        return self

