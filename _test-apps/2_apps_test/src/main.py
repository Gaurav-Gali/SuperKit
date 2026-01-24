from superkit import create_app
from config.settings import settings

dev = create_app(
    settings=settings,
    environment=settings.environment,
).mount_apps(
    include=['posts']
)