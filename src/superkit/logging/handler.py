import logging
from rich.console import Console

from superkit.logging.record import SuperKitLogRecord
from superkit.logging.renderers.user import UserPanelRenderer
from superkit.logging.renderers.http import HttpPanelRenderer
from superkit.logging.renderers.json import JsonPanelRenderer
from superkit.logging.renderers.error import ErrorPanelRenderer
from superkit.logging.filters.noise import NOISE_PHRASES

console = Console()


class SuperKitPanelHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.user_renderer = UserPanelRenderer()
        self.http_renderer = HttpPanelRenderer()
        self.json_renderer = JsonPanelRenderer()
        self.error_renderer = ErrorPanelRenderer()

    def emit(self, record: logging.LogRecord):
        try:
            message = record.getMessage().lower()

            if record.name == "uvicorn.error":
                if any(p in message for p in NOISE_PHRASES):
                    return
                # If uvicorn.error has exception info, show the error
                if record.exc_info:
                    console.print(self.error_renderer.render(*record.exc_info))
                    return

            if record.name == "uvicorn.access":
                panel_record = self._convert_uvicorn_access(record)
                if panel_record:
                    console.print(self.http_renderer.render(panel_record))
                return

            payload = record.msg
            if isinstance(payload, SuperKitLogRecord):
                console.print(self._render(payload))

            # Handle any other log record with exception info
            elif record.exc_info:
                console.print("\n")
                console.print(self.error_renderer.render(*record.exc_info))

        except Exception:
            self.handleError(record)

    def _convert_uvicorn_access(self, record: logging.LogRecord):
        msg = record.getMessage()
        try:
            # Parse: 127.0.0.1:54321 - "GET /api/users HTTP/1.1" 200
            parts = msg.split('"')

            # Client info (before the quoted part)
            client = parts[0].strip().rstrip(' -')

            # Request line
            request_part = parts[1]
            method, path, protocol = request_part.split()

            # Status code
            status_part = parts[2].strip().split()
            status = status_part[0]

        except Exception as e:
            return None

        return SuperKitLogRecord(
            kind="http",
            level="INFO",
            title=f"{method} {path}",
            meta={
                "method": method,
                "path": path,
                "status": status,
                "client": client,
                "protocol": protocol,
            },
        )

    def _render(self, record: SuperKitLogRecord):
        if record.kind == "http":
            return self.http_renderer.render(record)
        if record.kind == "json":
            return self.json_renderer.render(record)
        return self.user_renderer.render(record)

