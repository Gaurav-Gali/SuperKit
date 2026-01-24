# CLI Overview

SuperKit provides a powerful command-line interface for managing your projects and running your applications.

---

## Available Commands

| Command         | Description                           |
| --------------- | ------------------------------------- |
| `superkit init` | Initialize a new SuperKit project     |
| `superkit run`  | Run your SuperKit/FastAPI application |

---

## Quick Reference

### Initialize a Project

```bash
superkit init my-apps
```

Creates a new SuperKit project with the recommended structure.

[Learn more →](commands/init.md)

### Run Your Application

```bash
superkit run apps
```

Starts your application with hot reload and beautiful console output.

[Learn more →](commands/run.md)

---

## Global Options

### Help

Get help for any command:

```bash
superkit --help
superkit init --help
superkit run --help
```

### Version

Check SuperKit version:

```bash
superkit --version
```

---

## Common Workflows

### Starting a New Project

```bash
# Create project
superkit init my-apps

# Navigate to project
cd my-apps

# Run the apps
superkit run apps
```

### Development Workflow

```bash
# Run with auto-reload (default)
superkit run apps

# Run on custom port
superkit run apps --port 3000

# Run on all interfaces
superkit run apps --host 0.0.0.0
```

### Multiple Environments

```bash
# Define multiple apps instances in main.py
# dev = SuperKitApp(environment="development")
# prod = SuperKitApp(environment="production")

# Run development
superkit run dev

# Run production
superkit run prod --no-reload
```

---

## Features

### 🎨 Beautiful Output

SuperKit CLI provides rich, colorful console output:

- Server information panels
- Colored log messages
- Formatted tables and JSON
- Clear error messages

### ⚡ Hot Reload

Development server automatically reloads when you change code:

```bash
superkit run apps  # Auto-reload enabled by default
```

### 🔧 Configuration

Override settings from the command line:

```bash
superkit run apps --host 0.0.0.0 --port 3000 --no-reload
```

### ✅ Validation

SuperKit validates your project structure and configuration before running.

---

## Next Steps

<div class="grid cards" markdown>

- **init Command**

  Create new SuperKit projects

  [Learn More →](commands/init.md)

- **run Command**

  Run your applications

  [Learn More →](commands/run.md)

</div>
