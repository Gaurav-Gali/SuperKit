from pathlib import Path
from jinja2 import Template


def render_template_dir(template_dir: Path, target_dir: Path, context: dict):
    for path in template_dir.rglob("*"):
        relative = path.relative_to(template_dir)
        dest = target_dir / relative

        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue

        if path.suffix == ".template":
            dest = dest.with_suffix("")
            content = path.read_text()
            rendered = Template(content).render(**context)
            dest.write_text(rendered)
        else:
            dest.write_bytes(path.read_bytes())
