from apps.posts.controllers.comments import router

@router.get("{c_id}")
def comments(c_id:int):
    return {
        "c_id":c_id,
        "app" : "comments",
    }