### ==What is SuperKit==
SuperKit is a **FastAPI-native application framework** focused on:

- clean app isolation (Django-style apps)
    
- explicit lifecycle management
    
- predictable routing
    
- zero magic imports in user code
    
- strong DX with minimal boilerplate

Core philosophy:

- **Users declare intent**
    
- **SuperKit owns wiring**
    
- **Imports and side effects happen at controlled lifecycle stages**

<hr>

### ==Project Layout (Canonical)==
**`superkit init`**
<hr>
```md
my-superkit-app/
├── src/
│   ├── main.py
│   ├── config/
│   │   ├── settings.py
│   │   └── security.py
│   └── apps/
│       ├── __init__.py
│       ├── users/
│       │   ├── __init__.py
│       │   ├── app.py
│       │
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   └── user.py
│       │   │
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   └── user.py
│       │   │
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   └── user_service.py
│       │   │
│       │   └── controllers/
│       │       ├── __init__.py
│       │       ├── users.py
│       │       └── posts/
│       │           ├── __init__.py
│       │           └── posts.py
│       │
│       └── data/
│           ├── __init__.py
│           ├── app.py
│           └── controllers/
│               ├── __init__.py
│               └── data.py
├── .env
└── pyproject.toml
```

Key rules:

- `src/` is the import root
    
- `apps/` contains domain apps
    
- Each app is fully isolated
    
- No cross-app imports at import time

<hr>

### Running the project
```bash
superkit run dev
```
