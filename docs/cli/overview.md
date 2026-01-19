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
superkit init my-app
```

Creates a new SuperKit project with the recommended structure.

[Learn more →](commands/init.md)

### Run Your Application

```bash
superkit run app
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
superkit init my-app

# Navigate to project
cd my-app

# Run the app
superkit run app
```

### Development Workflow

```bash
# Run with auto-reload (default)
superkit run app

# Run on custom port
superkit run app --port 3000

# Run on all interfaces
superkit run app --host 0.0.0.0
```

### Multiple Environments

```bash
# Define multiple app instances in main.py
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
superkit run app  # Auto-reload enabled by default
```

### 🔧 Configuration

Override settings from the command line:

```bash
superkit run app --host 0.0.0.0 --port 3000 --no-reload
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
