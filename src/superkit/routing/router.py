from fastapi import APIRouter

class Router(APIRouter):
    def __init__(self, *, path: str = "", **kwargs):
        if path:
            path = str(path)
            if not path.startswith("/"):
                path = "/" + path
        super().__init__(prefix=path, **kwargs)
