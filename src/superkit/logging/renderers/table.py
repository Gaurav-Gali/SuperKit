from rich.table import Table
from rich.box import SIMPLE, ROUNDED, MINIMAL


class TableRenderer:
    """Renders tabular data as a Rich Table"""

    def __init__(
            self,
            show_header: bool = True,
            header_style: str = "bold cyan",
            border_style: str = "dim",
            row_styles: list[str] = None,
            box_style=ROUNDED,
    ):
        self.show_header = show_header
        self.header_style = header_style
        self.border_style = border_style
        self.row_styles = row_styles or ["", "dim"]  # Alternating row styles
        self.box_style = box_style

    def render(self, data: list[list]) -> Table:
        """
        Render a 2D list as a Rich Table.

        Args:
            data: 2D list where first row is headers, remaining rows are data
                  Example: [["Name", "Age"], ["Alice", 30], ["Bob", 25]]

        Returns:
            Rich Table object
        """
        if not data or len(data) == 0:
            return self._empty_table()

        # Separate headers and rows
        headers = data[0] if len(data) > 0 else []
        rows = data[1:] if len(data) > 1 else []

        # Create table
        table = Table(
            show_header=self.show_header,
            header_style=self.header_style,
            border_style=self.border_style,
            box=self.box_style,
            padding=(0, 1),
            expand=False,
        )

        # Add columns
        for header in headers:
            table.add_column(
                str(header),
                justify="left",
                no_wrap=False,
            )

        # Add rows with alternating styles
        for idx, row in enumerate(rows):
            style = self.row_styles[idx % len(self.row_styles)]
            table.add_row(
                *[str(cell) for cell in row],
                style=style
            )

        return table

    def _empty_table(self) -> Table:
        """Return an empty table with a message"""
        table = Table(
            show_header=False,
            border_style=self.border_style,
            box=self.box_style,
        )
        table.add_column("Message")
        table.add_row("[dim italic]No data to display[/]")
        return table