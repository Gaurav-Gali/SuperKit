### ==App Definition==

Each app **must** define exactly one `AppConfig` subclass.

`apps/users/app.py`
<hr>
```python
from superkit.apps import AppConfig
from apps.users.controllers import router as user_router

class UsersApp(AppConfig):
    name = "users"
    url_prefix = "/users"
    tags = ["Users"]
    routers = [user_router]
```

Rules enforced:

- Exactly one AppConfig per app
    
- No magic names
    
- No implicit discovery

<hr>

### ==App Discovery==
SuperKit discovers apps from the filesystem.

Rules:

- Apps live under `apps/`
    
- Must be a package
    
- Must contain `app.py`
    
- Controllers are **not** imported during discovery

This ensures:

- Safe startup
    
- No accidental side effects
    
- Predictable mounting

