import logging
from superkit.logging.record import SuperKitLogRecord

_logger = logging.getLogger("superkit.app")


class _LogAPI:
    def info(self, *, title: str, message: str):
        _logger.info(
            SuperKitLogRecord(
                kind="user",
                level="INFO",
                title=title,
                message=message,
            )
        )

    def warning(self, *, title: str, message: str):
        _logger.warning(
            SuperKitLogRecord(
                kind="user",
                level="WARNING",
                title=title,
                message=message,
            )
        )

    def error(self, *, title: str, message: str):
        _logger.error(
            SuperKitLogRecord(
                kind="user",
                level="ERROR",
                title=title,
                message=message,
            )
        )

    def json(self, *, title: str, data: dict):
        _logger.info(
            SuperKitLogRecord(
                kind="json",
                level="INFO",
                title=title,
                data=data,
            )
        )


log = _LogAPI()
