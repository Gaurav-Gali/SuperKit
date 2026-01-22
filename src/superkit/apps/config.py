from importlib import import_module
from fastapi import APIRouter


class AppConfig:
    name: str
    url_prefix: str
    tags: list[str] = []
    routers: list[APIRouter] = []

    def _derive_controller_packages(self) -> set[str]:
        """
        Derive controller packages from router module paths.
        """
        packages = set()

        for router in self.routers:
            module = router.__module__

            # Strip trailing ".<filename>" if present
            # e.g. apps.users.controllers.posts -> apps.users.controllers.posts
            packages.add(module)

        return packages

    def _load_controllers(self):
        for pkg in self._derive_controller_packages():
            import_module(pkg)

    def build_router(self) -> APIRouter:
        self._load_controllers()

        app_router = APIRouter(
            prefix=self.url_prefix,
            tags=self.tags,
        )

        for router in self.routers:
            app_router.include_router(router)

        return app_router
