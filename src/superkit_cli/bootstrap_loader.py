import sys
import importlib
from pathlib import Path
import typer

from superkit.runtime.registry import runtime

def bootstrap_loader() -> None:
    """
    Prepare the SuperKit runtime by:
    - treating CWD as project root
    - using src/ as import root
    - importing src/main.py
    - validating runtime initialization
    """

    project_root = Path.cwd()
    src_dir = project_root / "src"
    main_file = src_dir / "main.py"

    # ─────────────────────────────────────────────
    # Validate structure
    # ─────────────────────────────────────────────
    if not src_dir.exists():
        typer.secho(
            "Error: src/ directory not found.\n"
            "Expected project structure:\n"
            "  src/main.py",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if not main_file.exists():
        typer.secho(
            "Error: src/main.py not found.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # ─────────────────────────────────────────────
    # Ensure src/ is importable
    # ─────────────────────────────────────────────
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # ─────────────────────────────────────────────
    # Import main.py to initialize runtime
    # ─────────────────────────────────────────────
    try:
        importlib.import_module("main")
    except Exception as e:
        typer.secho(
            f"Error importing src/main.py: {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # ─────────────────────────────────────────────
    # Validate runtime
    # ─────────────────────────────────────────────
    if not runtime.is_initialized():
        typer.secho(
            "Error: SuperKit runtime was not initialized.\n"
            "Make sure create_app() is called in src/main.py.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
