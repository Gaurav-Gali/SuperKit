# Attachments

Attachments allow you to add structured data (JSON) and tables to your logs for better debugging and visualization.

---

## Overview

SuperKit logs support two types of attachments:

- **JSON** - Pretty-printed JSON data
- **Tables** - Formatted tables with headers and rows

Both can be added to any log level and can be chained together.

---

## JSON Attachments

### Basic Usage

```python
from superkit.logging.api.log import log

user = {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

log.info(title="User Data").add_json(user)
```

### With Title

Add a title to your JSON attachment:

```python
log.info(title="User Login").add_json(
    user,
    title="User Details"
)
```

### API Reference

```python
add_json(data: dict, title: str = None) -> LogEntry
```

**Parameters:**

- `data` (dict): Dictionary to display as JSON
- `title` (str, optional): Title for the JSON section

**Returns:** `LogEntry` for chaining

---

## Table Attachments

### Basic Usage

```python
from superkit.logging.api.log import log

data = [
    ["ID", "Name", "Status"],
    ["1", "Alice", "Active"],
    ["2", "Bob", "Inactive"],
    ["3", "Charlie", "Active"],
]

log.info(title="User List").add_table(data)
```

### With Title

Add a title to your table:

```python
log.info(title="Query Results").add_table(
    data,
    title="Active Users"
)
```

### API Reference

```python
add_table(data: list[list], title: str = None) -> LogEntry
```

**Parameters:**

- `data` (list[list]): 2D list where first row is headers
- `title` (str, optional): Title for the table section

**Returns:** `LogEntry` for chaining

---

## Chaining Attachments

You can chain multiple attachments to a single log:

```python
summary = {"total": 100, "active": 75, "inactive": 25}

details = [
    ["Status", "Count", "Percentage"],
    ["Active", "75", "75%"],
    ["Inactive", "25", "25%"],
]

log.info(title="User Report") \
    .add_json(summary, title="Summary") \
    .add_table(details, title="Breakdown")
```

---

## Examples

### User Data

```python
user = {
    "id": 456,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2024-01-15",
    "is_active": True
}

log.info(title="User Created").add_json(user, title="New User")
```

### API Response

```python
response = {
    "status": "success",
    "data": {
        "id": 789,
        "name": "Product A"
    },
    "timestamp": "2024-01-15T10:30:00Z"
}

log.info(title="API Call").add_json(response, title="Response")
```

### Query Results

```python
results = [
    ["ID", "Product", "Price", "Stock"],
    ["1", "Laptop", "$999", "15"],
    ["2", "Mouse", "$29", "150"],
    ["3", "Keyboard", "$79", "45"],
]

log.info(title="Inventory Check").add_table(results, title="Products")
```

### Error Details

```python
error_info = {
    "error_code": "DB_CONNECTION_FAILED",
    "message": "Unable to connect to database",
    "timestamp": "2024-01-15T10:30:00Z",
    "retry_count": 3
}

log.critical(title="Database Error").add_json(
    error_info,
    title="Error Details"
)
```

---

## In FastAPI Routes

### Logging Request Data

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(title="My API")

@app.post("/users")
def create_user(user: dict):
    log.info(title="User Creation Request").add_json(
        user,
        title="Request Body"
    )

    # Your logic
    new_user = save_user(user)

    log.info(title="User Created").add_json(
        new_user,
        title="Created User"
    )

    return new_user
```

### Logging Query Results

```python
@app.get("/users")
def list_users():
    users = get_all_users()

    # Log as table
    table_data = [["ID", "Name", "Email"]]
    for user in users:
        table_data.append([
            str(user["id"]),
            user["name"],
            user["email"]
        ])

    log.info(title="Users Retrieved").add_table(
        table_data,
        title="User List"
    )

    return users
```

### Logging with Summary and Details

```python
@app.get("/analytics")
def get_analytics():
    stats = calculate_stats()
    details = get_detailed_breakdown()

    summary = {
        "total_users": stats["total"],
        "active_users": stats["active"],
        "conversion_rate": stats["conversion"]
    }

    breakdown = [
        ["Metric", "Value", "Change"],
        ["Users", "1,234", "+12%"],
        ["Revenue", "$45,678", "+8%"],
        ["Orders", "567", "+15%"],
    ]

    log.info(title="Analytics Report") \
        .add_json(summary, title="Summary") \
        .add_table(breakdown, title="Details")

    return {"summary": summary, "breakdown": breakdown}
```

---

## Advanced Examples

### Nested JSON

```python
complex_data = {
    "user": {
        "id": 123,
        "profile": {
            "name": "John Doe",
            "age": 30,
            "address": {
                "city": "New York",
                "country": "USA"
            }
        }
    },
    "metadata": {
        "created": "2024-01-15",
        "updated": "2024-01-20"
    }
}

log.info(title="Complex Data").add_json(complex_data)
```

### Dynamic Tables

```python
def log_query_results(results):
    if not results:
        log.warning(title="No Results", message="Query returned no data")
        return

    # Build table dynamically
    headers = list(results[0].keys())
    rows = [headers]

    for result in results:
        rows.append([str(result[key]) for key in headers])

    log.info(title="Query Results").add_table(rows)

# Usage
users = [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"},
]

log_query_results(users)
```

### Comparison Tables

```python
comparison = [
    ["Feature", "Plan A", "Plan B", "Plan C"],
    ["Price", "$10", "$20", "$30"],
    ["Users", "5", "10", "Unlimited"],
    ["Storage", "10GB", "50GB", "100GB"],
    ["Support", "Email", "Email + Chat", "24/7 Phone"],
]

log.info(title="Pricing Comparison").add_table(
    comparison,
    title="Available Plans"
)
```

---

## Best Practices

!!! tip "Use Titles for Context"
Always add titles to attachments for clarity:

    ```python
    log.info(title="User Data").add_json(user, title="User Details")
    ```

!!! tip "Keep JSON Clean"
Remove sensitive or unnecessary data before logging:

    ```python
    # Bad
    log.info().add_json(user)  # Includes password field

    # Good
    safe_user = {k: v for k, v in user.items() if k != "password"}
    log.info().add_json(safe_user)
    ```

!!! tip "Format Tables Properly"
First row should always be headers:

    ```python
    data = [
        ["Header1", "Header2"],  # Headers
        ["Value1", "Value2"],    # Data
    ]
    ```

!!! tip "Combine for Rich Context"
Use both JSON and tables for comprehensive logging:

    ```python
    log.info(title="Report") \
        .add_json(summary) \
        .add_table(details)
    ```

!!! warning "Watch Data Size"
Large datasets can clutter console output. Consider:

    ```python
    # Bad - logs 1000 rows
    log.info().add_table(all_users)

    # Good - logs summary
    log.info().add_json({"total": len(all_users), "sample": all_users[:5]})
    ```

---

## Complete Example

```python
from superkit import SuperKitApp
from superkit.logging.api.log import log

app = SuperKitApp(title="E-commerce API")

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    log.info(
        title="Order Lookup",
        message=f"Fetching order {order_id}"
    )

    order = fetch_order(order_id)

    # Log order summary
    summary = {
        "order_id": order["id"],
        "customer": order["customer_name"],
        "total": order["total"],
        "status": order["status"]
    }

    # Log order items as table
    items = [["Product", "Quantity", "Price"]]
    for item in order["items"]:
        items.append([
            item["name"],
            str(item["quantity"]),
            f"${item['price']}"
        ])

    log.info(title="Order Retrieved") \
        .add_json(summary, title="Order Summary") \
        .add_table(items, title="Order Items")

    return order

@app.post("/orders")
def create_order(order: dict):
    log.info(title="Creating Order").add_json(
        order,
        title="Order Request"
    )

    # Process order
    new_order = process_order(order)

    # Log result
    result = {
        "order_id": new_order["id"],
        "status": "created",
        "total": new_order["total"]
    }

    log.info(title="Order Created").add_json(
        result,
        title="Order Confirmation"
    )

    return new_order
```

---

## Next Steps

- **[User Logs](user-logs.md)** - Learn about basic logging
- **[Advanced Logging](advanced.md)** - Custom renderers and features
- **[Overview](overview.md)** - Back to logging overview
