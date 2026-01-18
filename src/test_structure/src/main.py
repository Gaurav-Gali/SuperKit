from superkit import create_app
from settings import settings

dev = create_app(environment="new_environment", settings=settings)
