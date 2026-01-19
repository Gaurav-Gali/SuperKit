from datetime import datetime
from rich.panel import Panel
from rich.text import Text

from superkit.logging.styles.defaults import HTTP_COLORS, STATUS_COLORS, STATUS_TEXT


class HttpPanelRenderer:
    def render(self, record):
        time = datetime.now().strftime("%H:%M:%S")
        method = record.meta.get("method", "HTTP")
        path = record.meta.get("path", "")
        status = record.meta.get("status", "")
        client = record.meta.get("client", "")
        protocol = record.meta.get("protocol", "")

        color = HTTP_COLORS.get(method, "white")
        title = f"{method} • {time}"

        body = Text()

        # First line: Status and Path
        status_str = self._format_status(status)
        body.append(status_str, style=f"{self._get_status_color(status)} bold")
        body.append(" - ", style="dim")
        body.append(path, style="cyan bold")

        # Second line: Protocol and Client
        body.append("\n")
        if protocol:
            body.append(protocol, style="dim white")

        if client:
            if protocol:
                body.append(" - ", style="dim")
            body.append(client, style="dim")

        return Panel(
            body,
            title=title,
            border_style=color,
            title_align="left",
            padding=(1, 2),
        )

    def _format_status(self, status):
        """Format status code with text (e.g., '200 OK')"""
        try:
            code = int(status)
            text = STATUS_TEXT.get(code, "")
            return f"{code} {text}".strip() if text else str(code)
        except (ValueError, TypeError):
            return str(status)

    def _get_status_color(self, status):
        """Return color based on HTTP status code"""
        try:
            code = int(status)
            if 200 <= code < 300:
                return STATUS_COLORS["2xx"]
            elif 300 <= code < 400:
                return STATUS_COLORS["3xx"]
            elif 400 <= code < 500:
                return STATUS_COLORS["4xx"]
            elif 500 <= code < 600:
                return STATUS_COLORS["5xx"]
        except (ValueError, TypeError):
            pass
        return "white"

