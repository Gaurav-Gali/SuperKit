from importlib import import_module
from fastapi import APIRouter
from superkit.routing.controller_group import ControllerGroup


class AppConfig:
    name: str
    url_prefix: str
    tags: list[str] = []
    routers: list = []  # ControllerGroup | APIRouter

    def _unwrap_router(self, router):
        """
        Normalize routing surfaces into FastAPI routers.
        """
        if isinstance(router, ControllerGroup):
            return router._fastapi_router
        if isinstance(router, APIRouter):
            return router
        raise TypeError(
            f"Invalid router type: {type(router).__name__}. "
            "Expected ControllerGroup or APIRouter."
        )

    def _derive_controller_packages(self) -> set[str]:
        """
        Derive controller packages from router module paths.
        """
        packages = set()

        for r in self.routers:
            router = self._unwrap_router(r)
            packages.add(router.__module__)

        return packages

    def _load_controllers(self):
        for pkg in self._derive_controller_packages():
            import_module(pkg)

    def build_router(self) -> APIRouter:
        # Ensure all controllers are imported (decorators executed)
        self._load_controllers()

        app_router = APIRouter(
            prefix=self.url_prefix,
            tags=self.tags,
        )

        for r in self.routers:
            router = self._unwrap_router(r)
            app_router.include_router(router)

        return app_router
