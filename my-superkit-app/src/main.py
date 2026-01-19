from superkit import create_app
from config.settings import settings

app = (
    create_app(
        settings=settings,
        environment=settings.environment,
    )
)

