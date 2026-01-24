from apps.posts.controllers import router

@router.get("/")
async def list_posts():
    return {
        "app" : "posts"
    }