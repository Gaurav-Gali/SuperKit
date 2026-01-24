# superkit init

Initialize a new SuperKit project with the recommended structure and configuration.

---

## Usage

```bash
superkit init [PROJECT_NAME]
```

---

## Description

The `init` command creates a new SuperKit project with:

- Recommended directory structure
- Pre-configured `main.py` with SuperKitApp
- Settings file with sensible defaults
- Environment file template
- Project metadata (`pyproject.toml`)

---

## Interactive Setup

When you run `superkit init`, you'll be prompted with:

### 1. Project Name

```
Project name (or '.' for current directory):
```

- Enter a name for your project
- Use `.` to initialize in the current directory
- Creates a new directory with the project name

### 2. App Instance Name

```
App instance name (default: app):
```

- The variable name for your FastAPI app in `main.py`
- Default: `app`
- Examples: `app`, `dev`, `prod`, `api`

### 3. Environment

```
Environment (development/production):
```

- Choose your default environment
- Default: `development`
- Options: `development`, `production`

---

## Examples

### Create New Project

```bash
superkit init my-apps
```

Creates:

```
my-app/
├── src/
│   ├── main.py
│   └── settings.py
├── .env
├── .gitignore
└── pyproject.toml
```

### Initialize in Current Directory

```bash
mkdir my-project
cd my-project
superkit init .
```

Initializes SuperKit in the current directory.

### Custom Configuration

```bash
superkit init my-api
# Project name: my-api
# App instance: api
# Environment: production
```

---

## Generated Files

### `src/main.py`

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
    return {"message": "Hello from SuperKit!"}
```

### `src/settings.py`

```python
from superkit.settings import ProjectSettings

class Settings(ProjectSettings):
    title: str = "My App"
    description: str = "A SuperKit application"
    version: str = "0.1.0"
```

### `.env`

```bash
# Server Configuration
HOST=127.0.0.1
PORT=8000
RELOAD=true

# Application
ENVIRONMENT=development
DEBUG=true
```

### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "superkit",
]
```

---

## After Initialization

Once your project is created:

### 1. Navigate to Project

```bash
cd my-apps
```

### 2. Install Dependencies (if needed)

```bash
pip install -e .
# or
uv pip install -e .
```

### 3. Run Your Application

```bash
superkit run apps
```

### 4. Visit Your API

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Customization

After initialization, you can customize:

### Add Routes

Edit `src/main.py`:

```python
@app.get("/users")
def list_users():
    return {"users": []}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### Configure Settings

Edit `src/settings.py`:

```python
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    title: str = "My Custom API"
    version: str = "1.0.0"

    # Add custom settings
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
```

### Update Environment

Edit `.env`:

```bash
HOST=0.0.0.0
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key
```

---

## Error Handling

### Directory Not Empty

```
Error: Target directory is not empty.
```

**Solution:** Use an empty directory or initialize with `.` in an empty current directory.

### Permission Denied

```
Error: Permission denied
```

**Solution:** Ensure you have write permissions for the target directory.

---

## Best Practices

!!! tip "Use Version Control"
Initialize git after creating your project:

    ```bash
    cd my-app
    git init
    git add .
    git commit -m "Initial commit"
    ```

!!! tip "Create .env.example"
Create a template for environment variables:

    ```bash
    cp .env .env.example
    # Edit .env.example to remove sensitive values
    git add .env.example
    ```

!!! tip "Customize Immediately"
Update `settings.py` and `main.py` right after initialization to match your project needs.

---

## Complete Workflow

```bash
# 1. Create project
superkit init my-awesome-api

# 2. Navigate
cd my-awesome-api

# 3. Initialize git
git init

# 4. Create environment template
cp .env .env.example

# 5. Customize settings
# Edit src/settings.py and src/main.py

# 6. Run the apps
superkit run apps

# 7. Start coding!
```

---

## Next Steps

- **[Run Command](run.md)** - Learn how to run your application
- **[Project Structure](../../getting-started/project-structure.md)** - Understand the generated structure
- **[Settings](../../package/application/settings.md)** - Configure your application
