from superkit.apps import AppConfig
from apps.posts.controllers import router as posts_router


class PostsApp(AppConfig):
    name = "posts"
    url_prefix = "/posts"
    tags = ["Posts"]

    routers = [posts_router]