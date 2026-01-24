# Quick Start

Get your first SuperKit application running in under 5 minutes!

---

## 1. Create a New Project

Use the SuperKit CLI to scaffold a new project:

```bash
superkit init my-apps
```

You'll be prompted with a few questions:

- **Project name**: The name of your project (default: current directory)
- **App instance name**: The variable name for your app (default: `app`)
- **Environment**: Development or production (default: `development`)

---

## 2. Navigate to Your Project

```bash
cd my-apps
```

Your project structure will look like this:

```
my-app/
├── src/
│   ├── main.py          # Your application entry point
│   └── settings.py      # Configuration settings
├── .env                 # Environment variables
└── pyproject.toml       # Project dependencies
```

---

## 3. Explore the Generated Code

Open `src/main.py` to see your application:

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

---

## 4. Run Your Application

Start the development server:

```bash
superkit run apps
```

You'll see beautiful output showing:

- Server information (host, port, environment)
- Available endpoints
- Documentation URLs

---

## 5. Test Your API

Open your browser and visit:

- **API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 6. Add Logging

Let's add some logging to see SuperKit's beautiful console output:

```python
from superkit import SuperKitApp
from superkit.settings import ProjectSettings
from superkit.logging.api.log import log

settings = ProjectSettings()

app = SuperKitApp(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    environment=settings.environment,
)

@app.get("/")
def read_root():
    log.info(
        title="Root Endpoint",
        message="Someone visited the root endpoint!"
    )
    return {"message": "Hello from SuperKit!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user_data = {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com"
    }

    log.info(title="User Retrieved").add_json(
        user_data,
        title="User Data"
    )

    return user_data
```

Visit the endpoints and watch the beautiful console output! 🎨

---

## What's Next?

!!! success "Congratulations!"
You've created your first SuperKit application! Here's what to explore next:

- **[Project Structure](project-structure.md)** - Understand how SuperKit projects are organized
- **[Logging System](../package/logging/overview.md)** - Learn about rich logging features
- **[Settings Management](../package/application/settings.md)** - Configure your application
- **[CLI Commands](../cli/overview.md)** - Master the SuperKit CLI
