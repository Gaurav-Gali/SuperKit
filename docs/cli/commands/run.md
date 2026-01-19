# superkit run

Run your SuperKit/FastAPI application with hot reload and beautiful console output.

---

## Usage

```bash
superkit run [INSTANCE] [OPTIONS]
```

---

## Arguments

### INSTANCE (required)

The app instance name defined in `src/main.py`:

```bash
superkit run app
```

If you have multiple instances:

```python
# src/main.py
dev = SuperKitApp(environment="development")
prod = SuperKitApp(environment="production")
```

```bash
superkit run dev   # Run development instance
superkit run prod  # Run production instance
```

---

## Options

### `--host`

Override the host from settings:

```bash
superkit run app --host 0.0.0.0
```

**Default:** `127.0.0.1` (from settings)

### `--port`

Override the port from settings:

```bash
superkit run app --port 3000
```

**Default:** `8000` (from settings)

### `--reload / --no-reload`

Enable or disable auto-reload:

```bash
superkit run app --reload      # Enable auto-reload
superkit run app --no-reload   # Disable auto-reload
```

**Default:** `true` (from settings)

---

## Examples

### Basic Usage

```bash
superkit run app
```

Runs with default settings from `settings.py` and `.env`.

### Custom Host and Port

```bash
superkit run app --host 0.0.0.0 --port 3000
```

Runs on all interfaces at port 3000.

### Production Mode

```bash
superkit run prod --no-reload
```

Runs production instance without auto-reload.

### Development with Custom Port

```bash
superkit run dev --port 8080
```

Runs development instance on port 8080 with auto-reload.

---

## What Happens When You Run

### 1. Validation

SuperKit validates:

- `src/main.py` exists
- App instance exists and is a FastAPI app
- Configuration is valid

### 2. Bootstrap

Loads settings and configuration from:

- `src/settings.py`
- `.env` file
- Environment variables

### 3. Server Info Display

Shows beautiful server information:

```
┌─ SuperKit Server ─────────────────────────┐
│  App: My Awesome API                      │
│  Instance: app                            │
│  Environment: development                 │
│  URL: http://127.0.0.1:8000              │
│  Docs: http://127.0.0.1:8000/docs        │
│  Reload: enabled                          │
└───────────────────────────────────────────┘
```

### 4. Start Server

Starts Uvicorn with:

- Configured host and port
- Auto-reload (if enabled)
- SuperKit logging handlers

---

## Configuration Priority

Settings are resolved in this order (later overrides earlier):

1. **Default values** in `ProjectSettings`
2. **Custom settings** in `src/settings.py`
3. **`.env` file** values
4. **Environment variables**
5. **Command-line options** (highest priority)

Example:

```python
# settings.py
port: int = 8000  # 1. Default

# .env
PORT=3000  # 2. .env file

# Shell
export PORT=5000  # 3. Environment variable

# Command line
superkit run app --port 9000  # 4. CLI option (wins!)
```

Result: Server runs on port `9000`.

---

## Auto-Reload

When auto-reload is enabled (default in development):

- Server watches for file changes
- Automatically restarts when code changes
- Preserves your workflow

```bash
# Auto-reload enabled (default)
superkit run app

# Disable for production
superkit run app --no-reload
```

!!! tip "Auto-Reload in Development"
Keep auto-reload enabled during development for the best experience.

!!! warning "Disable in Production"
Always disable auto-reload in production:

    ```bash
    superkit run prod --no-reload
    ```

---

## Logging

SuperKit automatically configures logging:

### HTTP Requests

```
┌─ GET /api/users ──────────────────────────┐
│  Status: 200                              │
│  Client: 127.0.0.1:54321                  │
└───────────────────────────────────────────┘
```

### User Logs

```python
from superkit.logging.api.log import log

log.info(title="User Created", message="New user registered")
```

```
┌─ INFO • 14:23:45 ─────────────────────────┐
│  New user registered                      │
└───────────────────────────────────────────┘
```

### Errors

Exceptions are beautifully formatted with full tracebacks.

---

## Error Handling

### App Instance Not Found

```
Error: App instance 'myapp' not found in main.py
```

**Solution:** Check that the instance name matches what's in `src/main.py`.

### main.py Not Found

```
Error: src/main.py not found
```

**Solution:** Run the command from your project root directory.

### Not a FastAPI App

```
Error: 'myvar' exists but is not a FastAPI app
```

**Solution:** Ensure your instance is a `SuperKitApp` or `FastAPI` instance.

### Port Already in Use

```
Error: [Errno 48] Address already in use
```

**Solution:** Use a different port or kill the process using the port:

```bash
# Use different port
superkit run app --port 8001

# Or find and kill the process
lsof -ti:8000 | xargs kill
```

---

## Advanced Usage

### Multiple Environments

Define different instances for different environments:

```python
# src/main.py
from superkit import SuperKitApp
from settings import Settings

settings = Settings()

# Development instance
dev = SuperKitApp(
    title=f"{settings.title} (Dev)",
    environment="development",
    debug=True,
)

# Production instance
prod = SuperKitApp(
    title=settings.title,
    environment="production",
    debug=False,
)

# Add routes to both
@dev.get("/")
@prod.get("/")
def read_root():
    return {"message": "Hello!"}
```

Run:

```bash
superkit run dev   # Development
superkit run prod  # Production
```

### With Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

CMD ["superkit", "run", "prod", "--host", "0.0.0.0", "--no-reload"]
```

### With Process Managers

```bash
# PM2
pm2 start "superkit run prod --no-reload" --name api

# Supervisor
[program:api]
command=superkit run prod --no-reload
directory=/app
autostart=true
autorestart=true
```

---

## Best Practices

!!! tip "Use Different Instances"
Create separate instances for different environments:

    ```python
    dev = SuperKitApp(environment="development")
    prod = SuperKitApp(environment="production")
    ```

!!! tip "Override from CLI"
Use CLI options for temporary changes:

    ```bash
    superkit run app --port 3000  # Temporary port change
    ```

!!! tip "Use .env for Secrets"
Store sensitive configuration in `.env`:

    ```bash
    DATABASE_URL=postgresql://...
    SECRET_KEY=...
    ```

!!! warning "Production Checklist"
For production:

    - [ ] Disable auto-reload: `--no-reload`
    - [ ] Use production instance
    - [ ] Set `DEBUG=false` in `.env`
    - [ ] Use proper host: `--host 0.0.0.0`
    - [ ] Configure reverse proxy (nginx, etc.)

---

## Complete Example

```python
# src/settings.py
from superkit.settings import ProjectSettings
from pydantic import Field

class Settings(ProjectSettings):
    title: str = "My API"
    version: str = "1.0.0"
    database_url: str = Field(..., env="DATABASE_URL")

# src/main.py
from superkit import SuperKitApp
from superkit.logging.api.log import log
from settings import Settings

settings = Settings()

app = SuperKitApp(
    title=settings.title,
    version=settings.version,
    environment=settings.environment,
)

@app.on_event("startup")
def startup():
    log.info(
        title="Server Started",
        message=f"Running {settings.title} v{settings.version}"
    )

@app.get("/")
def read_root():
    log.info(title="Root Endpoint", message="Homepage accessed")
    return {"message": "Hello, SuperKit!"}
```

```bash
# .env
HOST=127.0.0.1
PORT=8000
RELOAD=true
ENVIRONMENT=development
DATABASE_URL=sqlite:///./app.db
```

Run:

```bash
superkit run app
```

---

## Next Steps

- **[Init Command](init.md)** - Create new projects
- **[Settings](../../package/application/settings.md)** - Configure your app
- **[Logging](../../package/logging/overview.md)** - Add beautiful logs
