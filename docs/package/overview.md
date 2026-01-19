# Package Overview

SuperKit provides a comprehensive set of tools and utilities built on top of FastAPI. This section covers how to use SuperKit's features in your application code.

---

## Core Components

### 🎯 **Application**

The `SuperKitApp` class extends FastAPI with additional features and conventions.

```python
from superkit import SuperKitApp

app = SuperKitApp(
    title="My API",
    environment="development"
)
```

[Learn more about SuperKitApp →](application/superkitapp.md)

---

### ⚙️ **Settings**

Type-safe configuration management with Pydantic and environment variable support.

```python
from superkit.settings import ProjectSettings

class Settings(ProjectSettings):
    database_url: str
    secret_key: str

settings = Settings()
```

[Learn more about Settings →](application/settings.md)

---

### 📝 **Logging**

Beautiful, structured logging with rich console output, JSON data, and tables.

```python
from superkit.logging.api.log import log

log.info(title="User Created", message="New user registered")
log.warning(title="Rate Limit", message="User approaching limit")
log.critical(title="System Error", message="Database connection failed")
```

[Learn more about Logging →](logging/overview.md)

---

## Quick Examples

### Basic Application

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings

settings = ProjectSettings()

app = SuperKitApp(
    title=settings.title,
    version=settings.version,
    environment=settings.environment,
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### With Logging

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(title="My API")

@app.get("/users/{user_id}")
def get_user(user_id: int):
    log.info(title="User Request", message=f"Fetching user {user_id}")

    # Your logic here
    user = {"id": user_id, "name": "John Doe"}

    log.info(title="User Found").add_json(user, title="User Data")

    return user
```

### With Settings

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    title: str = "My API"
    database_url: str = Field(..., env="DATABASE_URL")
    max_connections: int = 10

settings = Settings()

app = SuperKitApp(
    title=settings.title,
    environment=settings.environment,
)

@app.on_event("startup")
def startup():
    print(f"Connecting to: {settings.database_url}")
```

---

## Feature Matrix

| Feature         | Description                  | Documentation                      |
| --------------- | ---------------------------- | ---------------------------------- |
| **SuperKitApp** | Enhanced FastAPI application | [Docs](application/superkitapp.md) |
| **Settings**    | Configuration management     | [Docs](application/settings.md)    |
| **User Logs**   | Beautiful console logging    | [Docs](logging/user-logs.md)       |
| **Attachments** | JSON & table rendering       | [Docs](logging/attachments.md)     |

---

## Philosophy

SuperKit's package design follows these principles:

!!! tip "Explicit over Implicit"
Everything is imported and used explicitly. No auto-discovery or magic imports.

!!! tip "Type Safety First"
Full type hints throughout. Works perfectly with mypy and IDE autocomplete.

!!! tip "FastAPI Compatible"
All FastAPI features work as expected. SuperKit extends, never restricts.

---

## Next Steps

<div class="grid cards" markdown>

- **Application**

  Learn about `SuperKitApp` and settings management

  [Explore →](application/superkitapp.md)

- **Logging**

  Master SuperKit's beautiful logging system

  [Explore →](logging/overview.md)

</div>
