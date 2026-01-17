from typing import Optional, Dict, Any
from threading import Lock


class RuntimeRegistry:
    """
    Framework-owned runtime registry.

    Stores resolved configuration for the current process.
    """

    def __init__(self):
        self._lock = Lock()
        self._initialized = False
        self._settings: Optional[Dict[str, Any]] = None
        self._server: Optional[Dict[str, Any]] = None

    def initialize(
        self,
        *,
        settings: Dict[str, Any],
        server: Dict[str, Any],
    ) -> None:
        with self._lock:
            if self._initialized:
                raise RuntimeError("SuperKit runtime already initialized")

            self._settings = settings
            self._server = server
            self._initialized = True

    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def settings(self) -> Dict[str, Any]:
        if not self._initialized:
            raise RuntimeError("Runtime not initialized")
        return self._settings

    @property
    def server(self) -> Dict[str, Any]:
        if not self._initialized:
            raise RuntimeError("Runtime not initialized")
        return self._server

runtime = RuntimeRegistry()

