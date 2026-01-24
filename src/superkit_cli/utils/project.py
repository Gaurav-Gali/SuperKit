from pathlib import Path

def find_project_root(start: Path | None = None) -> Path:
    current = start or Path.cwd()

    for parent in [current, *current.parents]:
        if (parent / "apps").exists() or (parent / "src" / "apps").exists():
            return parent

    raise RuntimeError("Not inside a SuperKit project (apps/ folder not found)")


