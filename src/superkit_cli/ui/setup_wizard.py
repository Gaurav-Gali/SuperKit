from rich.console import Console

console = Console()


def setup_wizard() -> dict | None:
    console.print()

    # Project Name
    console.print("[cyan]Project name[/cyan] ([magenta]my-superkit-app[/magenta])")
    project_name = console.input("› ") or "my-superkit-app"
    console.print()

    # App Instance
    console.print("[cyan]App instance[/cyan] ([magenta]dev[/magenta])")
    app_instance = console.input("› ") or "dev"
    console.print()

    # Environment
    console.print("[cyan]Environment[/cyan] ([magenta]development[/magenta])")
    environment = console.input("› ") or "development"
    console.print()

    # Final Project Config
    config = {
        "project_name": project_name.strip(),
        "app_instance": app_instance.strip(),
        "environment": environment.strip(),
    }

    # Confirmation
    console.print()
    console.print("[green]Proceed?[/green] [dim](Y/n)[/dim]")
    confirmed = console.input("› ").lower() in ['y', 'yes']
    console.print()

    if not confirmed:
        return None

    return config