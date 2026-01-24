from superkit.routing import ControllerGroup

from apps.posts.controllers import router as parent_router

router = ControllerGroup(parent_router, "comments")
router.mount_controllers(
    __name__,
    __path__,
)