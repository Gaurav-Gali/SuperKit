from abc import ABC, abstractmethod
from rich.panel import Panel


class BasePanelRenderer(ABC):
    @abstractmethod
    def render(self, record) -> Panel:
        ...
