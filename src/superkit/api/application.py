from fastapi import FastAPI

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
    def mount_apps(self):
        return self

    def apply_security(self):
        return self

