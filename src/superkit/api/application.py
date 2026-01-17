from fastapi import FastAPI

class SuperKitApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)