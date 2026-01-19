from datetime import datetime
from rich.panel import Panel
from rich.json import JSON

class JsonPanelRenderer:
    def render(self, record):
        time = datetime.now().strftime("%H:%M:%S")
        title = f"JSON • {time}"

        json_render = JSON.from_data(record.data)

        return Panel(
            json_render,
            title=title,
            border_style="magenta",
        )

