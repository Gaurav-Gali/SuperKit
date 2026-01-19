from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class SuperKitLogRecord:
    kind: str
    level: str
    title: str
    message: Optional[str] = None
    data: Any = None
    meta: dict | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)
