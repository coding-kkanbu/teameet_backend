from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from kkanbu.board.views import (
    CategoryViewSet,
    CommentViewSet,
    PitAPatViewSet,
    PostViewSet,
)
from kkanbu.notification.views import NotificationViewSet
from kkanbu.operation.views import (
    CommentBlameViewSet,
    CommentLikeViewSet,
    PostBlameViewSet,
    PostLikeViewSet,
)
from kkanbu.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("category", CategoryViewSet)
router.register("post", PostViewSet, basename="Post")
router.register("comment", CommentViewSet, basename="Comment")
router.register("postlike", PostLikeViewSet, basename="PostLike")
router.register("commentlike", CommentLikeViewSet, basename="CommentLike")
router.register("postblame", PostBlameViewSet, basename="PostBlame")
router.register("commentblame", CommentBlameViewSet, basename="CommentBlame")
router.register("notification", NotificationViewSet, basename="Notification")
router.register("pitapat", PitAPatViewSet, basename="SogaetingOption")

app_name = "api"

urlpatterns = [
    path("v1/", include(router.urls)),
]
