from datetime import datetime
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.json import JSON
from rich.rule import Rule

from superkit.logging.styles.defaults import LEVEL_COLORS
from superkit.logging.renderers.table import TableRenderer


class UserPanelRenderer:
    def __init__(self):
        self.table_renderer = TableRenderer()
    
    def render(self, record):
        time = datetime.now().strftime("%H:%M:%S")
        color = LEVEL_COLORS.get(record.level, "white")

        title = f"{record.level} • {time}"
        
        renderables = []
        
        if record.message:
            message_text = Text(record.message, style="bold")
            renderables.append(message_text)
        
        if hasattr(record, 'attachments') and record.attachments:
            for i, attachment in enumerate(record.attachments):
                if i > 0 or record.message:
                    renderables.append(Rule(style="dim"))
                
                if attachment.get("title"):
                    title_text = Text(attachment["title"], style="italic dim")
                    renderables.append(title_text)
                    renderables.append(Text(""))
                
                if attachment["type"] == "json":
                    json_render = JSON.from_data(attachment["data"])
                    renderables.append(json_render)
                elif attachment["type"] == "table":
                    table = self.table_renderer.render(attachment["data"])
                    renderables.append(table)
        
        body = Group(*renderables) if len(renderables) > 1 else (renderables[0] if renderables else Text(""))

        return Panel(
            body,
            title=title,
            border_style=color,
            title_align="left",
            padding=(1, 2),
        )
