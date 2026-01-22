from superkit.routing.router import Router

class ControllerGroup:
    """
    A ControllerGroup represents a logical routing namespace.

    - Root group owns the real Router
    - Child groups share the same Router
    - Paths are auto-prefixed
    """

    def __init__(self, parent: "ControllerGroup | None" = None, prefix: str = ""):
        self._parent = parent
        self._prefix = prefix.strip("/")

        if parent is None:
            # root group owns the real router
            self._router = Router()
            self._full_prefix = ""
        else:
            # child group reuses parent's router
            self._router = parent._router
            self._full_prefix = self._join(parent._full_prefix, self._prefix)

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

    # ---- routing methods (delegation) ----

    def get(self, path: str, *args, **kwargs):
        return self._router.get(self._path(path), *args, **kwargs)

    def post(self, path: str, *args, **kwargs):
        return self._router.post(self._path(path), *args, **kwargs)

    def put(self, path: str, *args, **kwargs):
        return self._router.put(self._path(path), *args, **kwargs)

    def delete(self, path: str, *args, **kwargs):
        return self._router.delete(self._path(path), *args, **kwargs)



    # ---- internal hook for SuperKit ----
    @property
    def _fastapi_router(self) -> Router:
        """
        Exposes the underlying Router to SuperKit internals.
        Users should never rely on this.
        """
        return self._router
