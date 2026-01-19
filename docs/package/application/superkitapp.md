# SuperKitApp

`SuperKitApp` is the core application class that extends FastAPI with additional features and conventions.

---

## Basic Usage

```python
from superkit import SuperKitApp

app = SuperKitApp(
    title="My API",
    description="A powerful API built with SuperKit",
    version="1.0.0",
    environment="development",
)

@app.get("/")
def read_root():
    return {"message": "Hello, SuperKit!"}
```

---

## Constructor Parameters

### Required Parameters

None! All parameters are optional with sensible defaults.

### Optional Parameters

| Parameter     | Type          | Default          | Description                      |
| ------------- | ------------- | ---------------- | -------------------------------- |
| `title`       | `str`         | `"SuperKit App"` | API title shown in docs          |
| `description` | `str \| None` | `None`           | API description                  |
| `version`     | `str`         | `"0.1.0"`        | API version                      |
| `environment` | `str`         | `"development"`  | Environment name (semantic only) |

All standard FastAPI parameters are also supported:

```python
app = SuperKitApp(
    title="My API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
```

---

## Using with Settings

The recommended way is to use `SuperKitApp` with `ProjectSettings`:

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings

settings = ProjectSettings()

app = SuperKitApp(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    environment=settings.environment,
)
```

[Learn more about Settings →](settings.md)

---

## Environment Awareness

The `environment` parameter is semantic—it doesn't change behavior, but helps with organization:

```python
# Development instance
dev = SuperKitApp(
    title="My API (Dev)",
    environment="development",
)

# Production instance
prod = SuperKitApp(
    title="My API",
    environment="production",
)
```

Use different instances in your `main.py`:

```python
from superkit import SuperKitApp

dev = SuperKitApp(environment="development", debug=True)
prod = SuperKitApp(environment="production", debug=False)
```

Run with:

```bash
superkit run dev   # Development
superkit run prod  # Production
```

---

## Internal State

`SuperKitApp` maintains internal state for future features:

```python
app.state.installed_apps = None  # Reserved for app mounting
app.state.settings = None        # Reserved for settings
app.state.security = None        # Reserved for security
```

!!! info "Future Features"
These state attributes are reserved for upcoming SuperKit features and should not be modified directly.

---

## Lifecycle Methods

SuperKitApp provides chainable lifecycle methods:

```python
app = SuperKitApp(title="My API")

app.mount_apps()      # Reserved for future use
app.apply_security()  # Reserved for future use
```

!!! note "Coming Soon"
These methods are placeholders for future functionality. Currently, they return `self` for chaining.

---

## FastAPI Compatibility

`SuperKitApp` is a subclass of `FastAPI`, so all FastAPI features work:

### Routers

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return {"users": []}

app.include_router(router)
```

### Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
```

### Events

```python
@app.on_event("startup")
async def startup():
    print("Application starting...")

@app.on_event("shutdown")
async def shutdown():
    print("Application shutting down...")
```

### Dependencies

```python
from fastapi import Depends

def get_db():
    # Database connection logic
    pass

@app.get("/users")
def list_users(db=Depends(get_db)):
    return {"users": []}
```

---

## Complete Example

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings
from superkit.logging.api.log import log
from fastapi import APIRouter

# Settings
settings = ProjectSettings()

# Application
app = SuperKitApp(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    environment=settings.environment,
)

# Router
router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
def health_check():
    log.info(title="Health Check", message="System is healthy")
    return {"status": "healthy"}

@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = {"id": user_id, "name": "John Doe"}
    log.info(title="User Retrieved").add_json(user)
    return user

# Mount router
app.include_router(router)

# Lifecycle
@app.on_event("startup")
def startup():
    log.info(title="Startup", message=f"Starting {settings.title}")
```

---

## Next Steps

- **[Settings Management](settings.md)** - Configure your application
- **[Logging](../logging/overview.md)** - Add beautiful logging
- **[CLI Commands](../../cli/overview.md)** - Run your application
