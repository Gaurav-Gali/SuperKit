### ==ControllerGroup (Primary API)==
`ControllerGroup` is the **only routing abstraction users interact with**.

```python
from superkit.routing import ControllerGroup
```

Rules:

- Used everywhere (including root)
    
- One real router per app
    
- No nested FastAPI routers
    
- No `include_router` chains

<hr>

### ==One Router Per App (Critical Design)==
Internally:

- Each app has exactly **one FastAPI APIRouter**
    
- All ControllerGroups share it
    
- Prefix composition is string-based
    

Benefits:

- No prefix duplication bugs
    
- No router trees
    
- No timing issues
    
- Clean Swagger output

<hr>

### ==ControllerGroup Structure==

```python
from superkit.routing import ControllerGroup

router = ControllerGroup()                # root
router = ControllerGroup(parent, "posts") # subgroup
```

What it does:

- Shares the same underlying router
    
- Composes URL prefixes hierarchically
    
- Exposes route decorators:
    
    - `get`
        
    - `post`
        
    - `put`
        
    - `delete`

Users always write relative paths:

```python
from apps.users.controllers import router

@router.get("/")
def handler(): ...
```

<hr>

### ==Controller Mounting Lifecycle==
Controllers are **not imported automatically**.

They must be explicitly mounted.

#### API

```python
router = ControllerGroup()
# or router = ControllerGroup(<parent_controller>, "<sub-domain>")
router.mount_controllers(__name__, __path__, recursive=True|False)
```

#### Modes

#### Recursive mounting

`router.mount_controllers(__name__, __path__, recursive=True)`

- Mounts entire subtree
    
- Parent owns all children
    
- Ideal for large domains

#### Explicit mounting

`router.mount_controllers(__name__, __path__, recursive=False)`

- Only mounts current level
    
- Children must mount themselves
    
- Ideal for feature flags, versions

<hr>

### ==Idempotency Guarantees==
- Controllers cannot be mounted twice
    
- Apps cannot be mounted twice
    
- Safe against accidental re-calls
    
- Swagger never duplicates routes

<hr>

### ==Controller Discovery==
Controller discovery uses:

- `pkgutil.iter_modules`
    
- `importlib.import_module`
    

Rules:

- No `sys.modules` scanning
    
- No filesystem hacks
    
- No auto-imports at import time
    
- Side effects execute only during lifecycle

<hr>

### ==Swagger / OpenAPI Correctness==
Swagger shows **only routes that actually exist**.

SuperKit guarantees:

- Decorators execute before mounting
    
- Router state is final before FastAPI sees it
    
- No “endpoint missing” confusion

<hr>

### ==Router (Low-level Primitive)==

```python
from superkit.routing import Router
```

- Subclass of FastAPI `APIRouter`
    
- Supports `path` → `prefix` normalisation
    
- Public but **advanced**
    
- Not required for app development
    
- Used internally by ControllerGroup

