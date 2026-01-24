# Project Structure

Understanding how SuperKit projects are organized helps you build scalable applications.

---

## Default Structure

When you create a new SuperKit project with `superkit init`, you get this structure:

```
my-app/
├── src/
│   ├── main.py          # Application entry point
│   └── settings.py      # Configuration settings
├── .env                 # Environment variables
├── .gitignore          # Git ignore file
└── pyproject.toml      # Project metadata and dependencies
```

---

## Core Files

### `src/main.py`

The main application file where you define your FastAPI/SuperKit app:

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

@app.get("/")
def read_root():
    return {"message": "Hello, SuperKit!"}
```

!!! tip "Multiple App Instances"
You can define multiple app instances for different environments:

    ```python
    dev = SuperKitApp(environment="development")
    prod = SuperKitApp(environment="production")
    ```

### `src/settings.py`

Configuration management using Pydantic:

```python
from superkit.settings import ProjectSettings

class Settings(ProjectSettings):
    title: str = "My Awesome API"
    description: str = "Built with SuperKit"
    version: str = "1.0.0"

    # Add your custom settings
    database_url: str = "sqlite:///./apps.db"
    secret_key: str = "change-me-in-production"
```

### `.env`

Environment-specific variables:

```bash
# Server Configuration
HOST=127.0.0.1
PORT=8000
RELOAD=true

# Application
ENVIRONMENT=development
DEBUG=true

# Custom Settings
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key
```

---

## Recommended Structure (Growing Projects)

As your project grows, organize it like this:

```
my-app/
├── src/
│   ├── main.py
│   ├── settings.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── products.py
│   │   └── auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── email_service.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── test_api.py
│   └── test_services.py
├── .env
├── .env.example
└── pyproject.toml
```

---

## Directory Conventions

### `src/api/`

API route handlers organized by resource:

```python
# src/api/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return {"users": []}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Mount in `main.py`:

```python
from api.users import router as users_router

app.include_router(users_router)
```

### `src/models/`

Data models and schemas:

```python
# src/models/user.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
```

### `src/services/`

Business logic and external integrations:

```python
# src/services/user_service.py
from models.user import User

class UserService:
    def get_user(self, user_id: int) -> User:
        # Database logic here
        pass
```

### `src/utils/`

Helper functions and utilities:

```python
# src/utils/helpers.py
def format_date(date):
    return date.strftime("%Y-%m-%d")
```

---

## Best Practices

!!! tip "Keep `main.py` Clean"
Use `main.py` only for app initialization and router registration. Move business logic to services.

!!! tip "Use Absolute Imports"
Since SuperKit uses `src/` layout, configure your imports:

    ```python
    from api.users import router
    from models.user import User
    from services.user_service import UserService
    ```

!!! tip "Environment Files"
Keep `.env.example` with dummy values in version control, but never commit `.env`:

    ```bash
    # .gitignore
    .env
    ```

---

## Next Steps

- **[Package Overview](../package/overview.md)** - Learn about SuperKit's features
- **[Settings Guide](../package/application/settings.md)** - Deep dive into configuration
- **[Logging](../package/logging/overview.md)** - Add beautiful logging to your app
