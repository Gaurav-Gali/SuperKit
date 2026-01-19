# Logging Overview

SuperKit provides a beautiful, structured logging system with rich console output, perfect for development and debugging.

---

## Why SuperKit Logging?

Traditional logging is plain text and hard to read. SuperKit logging is:

- **🎨 Beautiful** - Colorful panels, formatted JSON, and tables
- **📊 Structured** - Attach JSON data and tables to any log
- **🎯 Simple** - Clean API with sensible defaults
- **⚡ Fast** - Built on Rich for high-performance rendering

---

## Quick Start

```python
from superkit.logging.api.log import log

# Simple logs
log.info(title="Server Started", message="Application is running")
log.warning(title="High Memory", message="Memory usage at 80%")
log.critical(title="Database Error", message="Connection failed")

# Logs with JSON data
log.info(title="User Created").add_json({
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
})

# Logs with tables
log.info(title="Query Results").add_table([
    ["ID", "Name", "Status"],
    ["1", "Alice", "Active"],
    ["2", "Bob", "Inactive"],
])
```

---

## Log Levels

SuperKit supports three log levels:

| Level        | Method           | Color  | Use Case                                    |
| ------------ | ---------------- | ------ | ------------------------------------------- |
| **INFO**     | `log.info()`     | Blue   | General information, success messages       |
| **WARNING**  | `log.warning()`  | Yellow | Warnings, deprecations, non-critical issues |
| **CRITICAL** | `log.critical()` | Red    | Errors, failures, critical problems         |

---

## Features

### User Logs

Beautiful panel-based logs with titles and messages:

```python
log.info(
    title="Request Processed",
    message="Successfully handled GET /api/users"
)
```

[Learn more →](user-logs.md)

### Attachments

Add JSON data and tables to any log:

```python
# JSON attachment
log.info(title="User Data").add_json(user_dict)

# Table attachment
log.info(title="Results").add_table(rows)

# Multiple attachments
log.info(title="Report") \
    .add_json(summary) \
    .add_table(details)
```

[Learn more →](attachments.md)

### Optional Parameters

Title and message are optional with sensible defaults:

```python
log.info()  # Title: "Info", Message: ""
log.warning()  # Title: "Warning", Message: ""
log.critical()  # Title: "Critical", Message: ""
```

---

## Visual Examples

### Simple Log

```python
log.info(title="Server Started", message="Listening on port 8000")
```

Output:

```
┌─ INFO • 14:23:45 ─────────────────────────┐
│  Listening on port 8000                   │
└───────────────────────────────────────────┘
```

### Log with JSON

```python
user = {"id": 1, "name": "Alice", "role": "admin"}
log.info(title="User Login").add_json(user, title="User Details")
```

Output:

```
┌─ INFO • 14:23:45 ─────────────────────────┐
│  ─────────────────────────────────────    │
│  User Details                             │
│                                           │
│  {                                        │
│    "id": 1,                               │
│    "name": "Alice",                       │
│    "role": "admin"                        │
│  }                                        │
└───────────────────────────────────────────┘
```

### Log with Table

```python
data = [
    ["ID", "Name", "Status"],
    ["1", "Alice", "Active"],
    ["2", "Bob", "Inactive"],
]
log.info(title="Users").add_table(data, title="User List")
```

Output:

```
┌─ INFO • 14:23:45 ─────────────────────────┐
│  ─────────────────────────────────────    │
│  User List                                │
│                                           │
│  ┌────┬───────┬──────────┐               │
│  │ ID │ Name  │ Status   │               │
│  ├────┼───────┼──────────┤               │
│  │ 1  │ Alice │ Active   │               │
│  │ 2  │ Bob   │ Inactive │               │
│  └────┴───────┴──────────┘               │
└───────────────────────────────────────────┘
```

---

## Integration with FastAPI

Use logging in your routes:

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(title="My API")

@app.get("/users/{user_id}")
def get_user(user_id: int):
    log.info(
        title="User Request",
        message=f"Fetching user {user_id}"
    )

    # Your logic
    user = {"id": user_id, "name": "John"}

    log.info(title="User Found").add_json(user)

    return user

@app.post("/users")
def create_user(user: dict):
    log.info(title="Creating User").add_json(user)

    # Your logic

    log.info(
        title="User Created",
        message=f"Successfully created user {user['name']}"
    )

    return user
```

---

## Best Practices

!!! tip "Use Descriptive Titles"
Make titles clear and actionable:

    ```python
    log.info(title="Database Connected")  # Good
    log.info(title="Info")  # Bad
    ```

!!! tip "Add Context with Attachments"
Include relevant data for debugging:

    ```python
    log.warning(title="Slow Query").add_json({
        "query": "SELECT * FROM users",
        "duration_ms": 1500,
        "threshold_ms": 1000,
    })
    ```

!!! tip "Use Appropriate Levels" - `info` - Normal operations, success - `warning` - Potential issues, deprecations - `critical` - Errors, failures

!!! warning "Don't Log Sensitive Data"
Never log passwords, tokens, or personal information:

    ```python
    # Bad
    log.info().add_json({"password": user.password})

    # Good
    log.info().add_json({"user_id": user.id})
    ```

---

## Next Steps

<div class="grid cards" markdown>

- **User Logs**

  Learn about basic logging with titles and messages

  [Learn More →](user-logs.md)

- **Attachments**

  Add JSON data and tables to your logs

  [Learn More →](attachments.md)

- **Advanced**

  Custom renderers and advanced features

  [Learn More →](advanced.md)

</div>
