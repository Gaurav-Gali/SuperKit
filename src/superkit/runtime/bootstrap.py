import sys
from pathlib import Path


def ensure_src_on_path():
    cwd = Path.cwd()
    src = cwd / "src"

    if src.exists() and src.is_dir():
        src_str = str(src)
        if src_str not in sys.path:
            sys.path.insert(0, src_str)
