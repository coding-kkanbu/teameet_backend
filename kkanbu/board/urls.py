from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)

urlpatterns = router.urls
