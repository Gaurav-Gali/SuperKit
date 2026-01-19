import logging
from superkit.logging.handler import SuperKitPanelHandler


def setup_logging():
    # Root logger (SuperKit owns logging)
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)
    root.addHandler(SuperKitPanelHandler())

    # Force uvicorn loggers to propagate to root
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
