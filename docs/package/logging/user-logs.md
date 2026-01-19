# User Logs

User logs are the primary way to output information in SuperKit. They display as beautiful colored panels in the console.

---

## Basic Usage

```python
from superkit.logging.api.log import log

log.info(title="Server Started", message="Application is running on port 8000")
log.warning(title="High Memory", message="Memory usage is at 85%")
log.critical(title="Database Error", message="Failed to connect to database")
```

---

## API Reference

### `log.info()`

Display informational messages (blue panel):

```python
log.info(title="User Created", message="Successfully created new user")
```

**Parameters:**

- `title` (str, optional): Log title. Default: `"Info"`
- `message` (str, optional): Log message. Default: `""`

**Returns:** `LogEntry` object for chaining attachments

---

### `log.warning()`

Display warning messages (yellow panel):

```python
log.warning(title="Rate Limit", message="User approaching rate limit")
```

**Parameters:**

- `title` (str, optional): Log title. Default: `"Warning"`
- `message` (str, optional): Log message. Default: `""`

**Returns:** `LogEntry` object for chaining attachments

---

### `log.critical()`

Display critical error messages (red panel):

```python
log.critical(title="System Error", message="Critical system failure")
```

**Parameters:**

- `title` (str, optional): Log title. Default: `"Critical"`
- `message` (str, optional): Log message. Default: `""`

**Returns:** `LogEntry` object for chaining attachments

---

## Optional Parameters

Both `title` and `message` are optional with sensible defaults:

```python
# No parameters - uses defaults
log.info()  # Title: "Info", Message: ""

# Only title
log.info(title="Server Started")

# Only message
log.info(message="Application is running")

# Both
log.info(title="Server Started", message="Application is running")
```

---

## Examples

### Simple Information

```python
log.info(title="Application Started", message="Server is ready")
```

### Success Message

```python
log.info(
    title="User Registered",
    message="New user account created successfully"
)
```

### Warning

```python
log.warning(
    title="Deprecated API",
    message="This endpoint will be removed in v2.0"
)
```

### Error

```python
log.critical(
    title="Database Connection Failed",
    message="Unable to connect to PostgreSQL"
)
```

---

## In FastAPI Routes

### Basic Route Logging

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(title="My API")

@app.get("/")
def read_root():
    log.info(title="Root Endpoint", message="Homepage accessed")
    return {"message": "Hello, World!"}
```

### Request Logging

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    log.info(
        title="User Request",
        message=f"Fetching user with ID: {user_id}"
    )

    # Your logic here
    user = {"id": user_id, "name": "John Doe"}

    return user
```

### Error Handling

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    log.info(title="User Lookup", message=f"Looking up user {user_id}")

    user = get_user_from_db(user_id)

    if not user:
        log.warning(
            title="User Not Found",
            message=f"No user found with ID {user_id}"
        )
        raise HTTPException(status_code=404, detail="User not found")

    log.info(title="User Found", message=f"Retrieved user {user.name}")
    return user
```

### Operation Tracking

```python
@app.post("/users")
def create_user(user: dict):
    log.info(title="Creating User", message=f"Creating user: {user['name']}")

    try:
        # Your creation logic
        new_user = save_user(user)

        log.info(
            title="User Created",
            message=f"Successfully created user {new_user.id}"
        )
        return new_user

    except Exception as e:
        log.critical(
            title="User Creation Failed",
            message=f"Error: {str(e)}"
        )
        raise
```

---

## Chaining with Attachments

Log entries return a `LogEntry` object that can be chained with attachments:

```python
# Add JSON data
log.info(title="User Data").add_json(user_dict)

# Add table
log.info(title="Results").add_table(rows)

# Multiple attachments
log.info(title="Report") \
    .add_json(summary_data) \
    .add_table(detail_rows)
```

[Learn more about attachments →](attachments.md)

---

## Automatic Emission

Logs are automatically emitted when the `LogEntry` object is destroyed:

```python
# Emitted immediately (no variable assignment)
log.info(title="Quick Log", message="This is emitted right away")

# Emitted when variable goes out of scope
entry = log.info(title="Delayed Log")
entry.add_json(data)
# Emitted here when entry is destroyed
```

You don't need to call any explicit emit method—it happens automatically!

---

## Best Practices

!!! tip "Use Descriptive Titles"
Titles should clearly indicate what happened:

    ```python
    log.info(title="Database Connected")  # Good
    log.info(title="Success")  # Bad
    ```

!!! tip "Include Context in Messages"
Messages should provide actionable information:

    ```python
    log.warning(
        title="Slow Query",
        message="Query took 1.5s (threshold: 1.0s)"
    )  # Good

    log.warning(title="Slow Query", message="Slow")  # Bad
    ```

!!! tip "Choose the Right Level" - **info**: Normal operations, success messages - **warning**: Potential issues, deprecations, non-critical problems - **critical**: Errors, failures, system problems

!!! warning "Don't Log Sensitive Data"
Never include passwords, tokens, or personal information in logs:

    ```python
    # Bad
    log.info(title="Login", message=f"Password: {password}")

    # Good
    log.info(title="Login", message=f"User {username} logged in")
    ```

---

## Complete Example

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log
from fastapi import HTTPException

app = SuperKitApp(title="User Management API")

@app.on_event("startup")
def startup():
    log.info(
        title="Application Started",
        message="User Management API is ready"
    )

@app.get("/users/{user_id}")
def get_user(user_id: int):
    log.info(
        title="User Lookup",
        message=f"Retrieving user {user_id}"
    )

    try:
        user = fetch_user(user_id)

        if not user:
            log.warning(
                title="User Not Found",
                message=f"No user with ID {user_id}"
            )
            raise HTTPException(status_code=404)

        log.info(
            title="User Retrieved",
            message=f"Found user: {user['name']}"
        )
        return user

    except Exception as e:
        log.critical(
            title="Database Error",
            message=f"Failed to fetch user: {str(e)}"
        )
        raise

@app.post("/users")
def create_user(user: dict):
    log.info(
        title="User Creation",
        message=f"Creating user: {user['name']}"
    )

    new_user = save_user(user)

    log.info(
        title="User Created",
        message=f"Successfully created user {new_user['id']}"
    )

    return new_user
```

---

## Next Steps

- **[Attachments](attachments.md)** - Add JSON and tables to logs
- **[Advanced Logging](advanced.md)** - Custom renderers and advanced features
- **[Overview](overview.md)** - Back to logging overview
