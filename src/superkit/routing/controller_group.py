from superkit.routing.router import Router
from superkit.routing.discovery import import_controllers


class ControllerGroup:
    """
    Logical routing namespace.

    - Root group owns the real Router
    - Child groups share the same Router
    - Paths are auto-prefixed
    - Controller mounting is explicit and idempotent
    """

    def __init__(self, parent=None, prefix: str = ""):
        self._parent = parent
        self._prefix = prefix.strip("/")
        self._mounted = False

        if parent is None:
            # root group owns the router
            self._router = Router()
            self._full_prefix = ""
        else:
            # child group reuses parent's router
            self._router = parent._router
            self._full_prefix = self._join(parent._full_prefix, self._prefix)

    # ---------- internal helpers ----------

    def _join(self, parent: str, child: str) -> str:
        if not parent:
            return child
        if not child:
            return parent
        return f"{parent}/{child}"

    def _path(self, path: str) -> str:
        path = path.strip("/")
        if not self._full_prefix:
            return f"/{path}" if path else "/"
        if not path:
            return f"/{self._full_prefix}"
        return f"/{self._full_prefix}/{path}"

    # ---------- lifecycle ----------

    def mount_controllers(
        self,
        package_name: str,
        package_path,
        *,
        recursive: bool = True,
    ) -> None:
        """
        Mount controller modules for this group.

        - Idempotent (safe to call multiple times)
        - recursive=True  → mounts entire subtree
        - recursive=False → mounts only this package
        """
        if self._mounted:
            return

        self._mounted = True
        import_controllers(
            package_name,
            package_path,
            recursive=recursive,
        )

    # ---------- routing surface ----------

    def get(self, path: str, *args, **kwargs):
        return self._router.get(self._path(path), *args, **kwargs)

    def post(self, path: str, *args, **kwargs):
        return self._router.post(self._path(path), *args, **kwargs)

    def put(self, path: str, *args, **kwargs):
        return self._router.put(self._path(path), *args, **kwargs)

    def delete(self, path: str, *args, **kwargs):
        return self._router.delete(self._path(path), *args, **kwargs)

    # ---------- framework hook ----------

    @property
    def _fastapi_router(self) -> Router:
        """
        Internal: exposes the real FastAPI router.
        SuperKit unwraps this automatically.
        """
        return self._router
