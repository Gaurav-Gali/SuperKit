from datetime import datetime
from rich.panel import Panel
from rich.text import Text

from superkit.logging.styles.defaults import LEVEL_COLORS


class UserPanelRenderer:
    def render(self, record):
        time = datetime.now().strftime("%H:%M:%S")
        color = LEVEL_COLORS.get(record.level, "white")

        title = f"{record.level} • {time}"
        body = Text(record.message or "")

        return Panel(
            body,
            title=title,
            border_style=color,
            title_align="left",
            padding=(0, 2),
        )
