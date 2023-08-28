from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .image.views import ImageViewSet
from .tag_anything.views import TagCategoryViewSet, TagViewSet
from .comment.views import CommentViewSet

router = DefaultRouter()
router.register("image", ImageViewSet, basename="Image")
router.register("tag", TagViewSet)
router.register("category", TagCategoryViewSet)
router.register(
    r"image/(?P<image_id>\d+)/comments", CommentViewSet, basename="Comment"
)

app_name = "v1"

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
