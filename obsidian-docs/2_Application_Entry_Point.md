### ==src/main.py==
```python
from superkit import create_app
from config.settings import settings

app = (
    create_app(
        settings=settings,
        environment=settings.environment,
    )
    .mount_apps(include_all=True)
)

```

**What happens here:**
- SuperKit runtime initializes
    
- No apps are mounted yet
    
- `mount_apps()` triggers app lifecycle
    
- Swagger becomes accurate only after mounting

### ==SuperKit App (extends FastAPI)==

Responsibilities:

- Holds runtime metadata
    
- Exposes lifecycle APIs
    
- Prevents illegal lifecycle usage

Key properties:

- `environment`
    
- `state.installed_apps`
    
- `_mounted_apps` (internal idempotency)
### ==Lifecycle APIs==

```python
app.mount_apps(...)
app.apply_security()
```

Rules:

- `mount_apps()` can be called **only once**
    
- All routing must be complete after mounting