from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def server_info(
    *,
    app_name: str,
    instance: str,
    host: str,
    port: int,
    reload: bool,
    environment: str = "development",
    docs_enabled: bool = True,
) -> None:
    console = Console()

    base_url = f"http://{host}:{port}"
    docs_url = f"{base_url}/docs"
    openapi_url = f"{base_url}/openapi.json"

    table = Table.grid(padding=(0, 3))
    table.add_column(style="bold cyan", justify="left")
    table.add_column(style="white", justify="left")

    # --- App / Server Info ---
    table.add_row("App", f"[bold]{app_name}[/bold]")
    table.add_row("Instance", instance)
    table.add_row("Environment", f"[magenta]{environment}[/magenta]")
    table.add_row(
        "Reload",
        "[green]Enabled[/green]" if reload else "[red]Disabled[/red]",
    )
    table.add_row("Host", host)
    table.add_row("Port", str(port))

    # Spacer
    table.add_row("", "")

    # --- URLs ---
    table.add_row(
        "Server",
        f"[link={base_url}]{base_url}[/link]",
    )

    if docs_enabled:
        table.add_row(
            "Docs",
            f"[link={docs_url}]{docs_url}[/link]",
        )
        table.add_row(
            "OpenAPI",
            f"[link={openapi_url}]{openapi_url}[/link]",
        )

    panel = Panel(
        table,
        title=Text(" SuperKit  •  Server Running ", style="black on green"),
        border_style="green",
        padding=(1, 2),
    )

    console.print(panel)
