# Settings Management

SuperKit provides powerful configuration management through `ProjectSettings`, built on Pydantic Settings.

---

## Basic Usage

```python
from superkit.settings import ProjectSettings

settings = ProjectSettings()

print(settings.title)        # "SuperKit App"
print(settings.host)         # "127.0.0.1"
print(settings.port)         # 8000
print(settings.environment)  # "development"
```

---

## Custom Settings

Extend `ProjectSettings` to add your own configuration:

```python
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    # Override defaults
    title: str = "My Awesome API"
    version: str = "1.0.0"

    # Add custom settings
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    max_connections: int = 10
    enable_cache: bool = True

settings = Settings()
```

---

## Available Settings

### FastAPI Metadata

| Setting       | Type          | Default          | Description     |
| ------------- | ------------- | ---------------- | --------------- |
| `title`       | `str`         | `"SuperKit App"` | API title       |
| `description` | `str \| None` | `None`           | API description |
| `version`     | `str`         | `"0.1.0"`        | API version     |

### Advanced FastAPI Configuration

| Setting          | Type             | Default | Description               |
| ---------------- | ---------------- | ------- | ------------------------- |
| `debug`          | `bool`           | `False` | Debug mode                |
| `lifespan`       | `object \| None` | `None`  | Lifespan context manager  |
| `fastapi_kwargs` | `dict`           | `{}`    | Additional FastAPI kwargs |

### Environment

| Setting       | Type  | Default         | Description      |
| ------------- | ----- | --------------- | ---------------- |
| `environment` | `str` | `"development"` | Environment name |

### Server Configuration

| Setting  | Type   | Default       | Description            |
| -------- | ------ | ------------- | ---------------------- |
| `host`   | `str`  | `"127.0.0.1"` | Server host            |
| `port`   | `int`  | `8000`        | Server port            |
| `reload` | `bool` | `True`        | Auto-reload on changes |

### Documentation URLs

| Setting       | Type          | Default           | Description        |
| ------------- | ------------- | ----------------- | ------------------ |
| `docs_url`    | `str \| None` | `"/docs"`         | Swagger UI URL     |
| `redoc_url`   | `str \| None` | `"/redoc"`        | ReDoc URL          |
| `openapi_url` | `str \| None` | `"/openapi.json"` | OpenAPI schema URL |

---

## Environment Variables

Settings automatically load from environment variables and `.env` files:

### `.env` File

```bash
# Server
HOST=0.0.0.0
PORT=3000
RELOAD=false

# Application
TITLE=Production API
VERSION=2.0.0
ENVIRONMENT=production
DEBUG=false

# Custom Settings
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=super-secret-key-change-in-production
MAX_CONNECTIONS=50
```

### Using Environment Variables

```python
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    max_connections: int = Field(default=10, env="MAX_CONNECTIONS")

settings = Settings()

# Values loaded from .env or environment
print(settings.database_url)  # From DATABASE_URL
print(settings.secret_key)    # From SECRET_KEY
print(settings.max_connections)  # From MAX_CONNECTIONS or default
```

---

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. **Default values** in your Settings class
2. **`.env` file** in the project root
3. **Environment variables** from the shell

```python
class Settings(ProjectSettings):
    port: int = 8000  # 1. Default

# 2. .env file
# PORT=3000

# 3. Environment variable
# export PORT=5000

settings = Settings()
print(settings.port)  # 5000 (environment variable wins)
```

---

## Using with SuperKitApp

The recommended pattern:

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings

# Define settings
settings = ProjectSettings()

# Create apps with settings
app = SuperKitApp(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    environment=settings.environment,
    debug=settings.debug,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
)
```

---

## Advanced Examples

### Multiple Environments

```python
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )

    # Email
    smtp_host: str = Field(default="localhost", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")

    # Feature Flags
    enable_cache: bool = Field(default=True, env="ENABLE_CACHE")
    enable_analytics: bool = Field(default=False, env="ENABLE_ANALYTICS")

settings = Settings()
```

### Validation

```python
from superkit.settings import ProjectSettings
from pydantic import Field, validator

class Settings(ProjectSettings):
    port: int = Field(ge=1, le=65535, env="PORT")
    max_connections: int = Field(ge=1, le=1000, env="MAX_CONNECTIONS")

    @validator("port")
    def validate_port(cls, v):
        if v < 1024:
            raise ValueError("Port must be >= 1024 for non-root users")
        return v

settings = Settings()
```

### Nested Configuration

```python
from superkit.settings import ProjectSettings
from pydantic import BaseModel, Field

class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = 10
    echo: bool = False

class Settings(ProjectSettings):
    database: DatabaseConfig = Field(
        default=DatabaseConfig(
            url="sqlite:///./apps.db",
            pool_size=5,
        )
    )

settings = Settings()
print(settings.database.url)
print(settings.database.pool_size)
```

---

## Best Practices

!!! tip "Use Type Hints"
Always provide type hints for better IDE support and validation:

    ```python
    database_url: str  # Good
    database_url = ""  # Bad
    ```

!!! tip "Required vs Optional"
Use `Field(...)` for required settings, provide defaults for optional:

    ```python
    secret_key: str = Field(..., env="SECRET_KEY")  # Required
    cache_ttl: int = 300  # Optional with default
    ```

!!! tip "Environment File Example"
Keep `.env.example` in version control with dummy values:

    ```bash
    # .env.example
    DATABASE_URL=postgresql://user:pass@localhost/db
    SECRET_KEY=change-me
    ```

!!! warning "Never Commit Secrets"
Add `.env` to `.gitignore`:

    ```bash
    # .gitignore
    .env
    ```

---

## Complete Example

```python
# src/settings.py
from superkit.settings import ProjectSettings
from pydantic import Field, PostgresDsn

class Settings(ProjectSettings):
    # Override defaults
    title: str = "My Production API"
    version: str = "1.0.0"

    # Database
    database_url: PostgresDsn = Field(..., env="DATABASE_URL")
    db_pool_size: int = Field(default=10, env="DB_POOL_SIZE")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External Services
    redis_url: str = Field(default="redis://localhost", env="REDIS_URL")
    smtp_host: str = Field(..., env="SMTP_HOST")

    # Feature Flags
    enable_cache: bool = True
    enable_rate_limiting: bool = True

# src/main.py
from superkit import SuperKitApp
from settings import Settings

settings = Settings()

app = SuperKitApp(
    title=settings.title,
    version=settings.version,
    environment=settings.environment,
)

@app.on_event("startup")
def startup():
    print(f"Connecting to: {settings.database_url}")
    print(f"Cache enabled: {settings.enable_cache}")
```

---

## Next Steps

- **[SuperKitApp](superkitapp.md)** - Use settings with your application
- **[Logging](../logging/overview.md)** - Add logging to your app
- **[CLI Commands](../../cli/commands/run.md)** - Run with different settings
