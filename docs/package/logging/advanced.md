# Advanced Logging

Advanced features and customization options for SuperKit's logging system.

---

## Architecture

SuperKit's logging system is built on Python's standard `logging` module with custom handlers and renderers.

### Components

- **Log API** (`log.info()`, `log.warning()`, `log.critical()`)
- **LogEntry** - Chainable entry object for attachments
- **SuperKitLogRecord** - Custom log record with metadata
- **Handlers** - Process and route log records
- **Renderers** - Format logs for console output

---

## Custom Renderers

SuperKit uses different renderers for different log types:

### User Panel Renderer

Renders user logs with panels:

```python
from superkit.logging.renderers.user import UserPanelRenderer

renderer = UserPanelRenderer()
```

### HTTP Panel Renderer

Automatically renders HTTP requests (from Uvicorn):

```python
from superkit.logging.renderers.http import HttpPanelRenderer

renderer = HttpPanelRenderer()
```

### Error Renderer

Renders exceptions and tracebacks:

```python
from superkit.logging.renderers.error import ErrorPanelRenderer

renderer = ErrorPanelRenderer()
```

---

## Log Record Structure

`SuperKitLogRecord` contains:

```python
class SuperKitLogRecord:
    kind: str          # "user", "http", "json", "error"
    level: str         # "INFO", "WARNING", "CRITICAL"
    title: str         # Log title
    message: str       # Log message
    attachments: list  # JSON/table attachments
    meta: dict         # Additional metadata
```

---

## Handler Configuration

The `SuperKitPanelHandler` processes all logs:

```python
from superkit.logging.handler import SuperKitPanelHandler
import logging

handler = SuperKitPanelHandler()
logger = logging.getLogger("superkit.app")
logger.addHandler(handler)
```

---

## Automatic HTTP Logging

SuperKit automatically logs HTTP requests from Uvicorn:

```
┌─ GET /api/users ──────────────────────────┐
│  Status: 200                              │
│  Client: 127.0.0.1:54321                  │
└───────────────────────────────────────────┘
```

This happens automatically when you run your app with `superkit run`.

---

## Noise Filtering

SuperKit filters out noisy Uvicorn messages:

```python
# Filtered phrases
NOISE_PHRASES = [
    "started server process",
    "waiting for application startup",
    "application startup complete",
    "uvicorn running on",
]
```

These are hidden to keep your console clean.

---

## Integration with Python Logging

SuperKit works with Python's standard logging:

```python
import logging
from superkit.logging.api.log import log

# Standard Python logging
logger = logging.getLogger(__name__)
logger.info("This is standard logging")

# SuperKit logging
log.info(title="SuperKit Log", message="This is SuperKit logging")
```

Both work together seamlessly!

---

## Best Practices

!!! tip "Use SuperKit Logs for User-Facing Output"
Use `log.info()` for output you want users to see:

    ```python
    log.info(title="Server Ready", message="Application started")
    ```

!!! tip "Use Standard Logging for Debug Info"
Use Python's logging for internal debugging:

    ```python
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("Internal debug info")
    ```

!!! tip "Let SuperKit Handle HTTP Logs"
Don't manually log HTTP requests—SuperKit does this automatically.

---

## Future Features

SuperKit's logging system is designed to support:

- Custom log kinds
- Log persistence
- Log filtering and search
- Remote logging
- Structured log export

Stay tuned for updates!

---

## Next Steps

- **[User Logs](user-logs.md)** - Basic logging guide
- **[Attachments](attachments.md)** - JSON and tables
- **[Overview](overview.md)** - Logging overview
