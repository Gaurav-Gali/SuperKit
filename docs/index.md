# Welcome to SuperKit

<div class="hero" markdown>

**SuperKit** is a batteries-included framework built on top of FastAPI that adds structure, conventions, and powerful tooling—without the magic.

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub](#){ .md-button }

</div>

---

## Why SuperKit?

FastAPI is excellent, but building production applications requires more than just a web framework. SuperKit provides:

### 🏗️ **Structure & Conventions**

Opinionated project structure that scales from prototypes to production without fighting the framework.

### 🎨 **Beautiful Logging**

Rich, colorful console output with support for JSON data, tables, and structured logging—all beautifully rendered.

### ⚙️ **Powerful CLI**

Intuitive command-line tools for project initialization, running servers, and managing your application.

### 🔧 **Configuration Management**

Type-safe settings with Pydantic, environment variable support, and sensible defaults.

### 🚀 **Developer Experience**

Hot reload, clear error messages, and tools designed to make development enjoyable.

---

## Quick Example

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(
    title="My Awesome API",
    environment="development"
)

@app.get("/")
def hello():
    log.info(title="Request Received", message="Hello endpoint called")
    return {"message": "Hello, SuperKit!"}
```

Run your app:

```bash
superkit run app
```

---

## Features at a Glance

| Feature                 | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| **FastAPI Foundation**  | Built on FastAPI—keep all the speed and async capabilities |
| **Rich Logging**        | Beautiful console output with JSON, tables, and colors     |
| **Type Safety**         | Full type hints and Pydantic integration                   |
| **CLI Tools**           | Project scaffolding and management commands                |
| **Settings Management** | Environment-based configuration with validation            |
| **Production Ready**    | Structured for scalability and maintainability             |

---

## What's Next?

<div class="grid cards" markdown>

- :material-clock-fast:{ .lg .middle } **Quick Start**

  ***

  Get up and running in minutes with our quick start guide.

  [Quick Start →](getting-started/quickstart.md)

- :material-book-open-variant:{ .lg .middle } **Package Usage**

  ***

  Learn how to use SuperKit's powerful features in your code.

  [Package Docs →](package/overview.md)

- :material-console:{ .lg .middle } **CLI Reference**

  ***

  Master the SuperKit command-line interface.

  [CLI Docs →](cli/overview.md)

</div>

---

## Philosophy

SuperKit follows these principles:

!!! tip "Convention over Configuration"
Sensible defaults that work out of the box, with full customization when needed.

!!! tip "No Magic"
Everything is explicit and understandable. No hidden behaviors or surprising side effects.

!!! tip "Developer Joy"
Beautiful output, clear errors, and tools that make development enjoyable.
