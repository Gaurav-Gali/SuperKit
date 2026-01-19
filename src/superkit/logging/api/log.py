import logging
from superkit.logging.record import SuperKitLogRecord

_logger = logging.getLogger("superkit.app")


class LogEntry:
    def __init__(self, record: SuperKitLogRecord, logger: logging.Logger):
        self._record = record
        self._logger = logger
        self._emitted = False
    
    def add_json(self, data: dict, title: str = None) -> "LogEntry":
        self._record.attachments.append({"type": "json", "data": data, "title": title})
        return self
    
    def add_table(self, data: list[list], title: str = None) -> "LogEntry":
        self._record.attachments.append({"type": "table", "data": data, "title": title})
        return self
    
    def _emit(self):
        if not self._emitted:
            log_method = getattr(self._logger, self._record.level.lower())
            log_method(self._record)
            self._emitted = True
    
    def __del__(self):
        self._emit()


class _LogAPI:
    def info(self, *, title: str = "Info", message: str = "") -> LogEntry:
        record = SuperKitLogRecord(
            kind="user",
            level="INFO",
            title=title,
            message=message,
        )
        return LogEntry(record, _logger)

    def warning(self, *, title: str = "Warning", message: str = "") -> LogEntry:
        record = SuperKitLogRecord(
            kind="user",
            level="WARNING",
            title=title,
            message=message,
        )
        return LogEntry(record, _logger)

    def critical(self, *, title: str = "Critical", message: str = "") -> LogEntry:
        record = SuperKitLogRecord(
            kind="user",
            level="CRITICAL",
            title=title,
            message=message,
        )
        return LogEntry(record, _logger)


log = _LogAPI()
