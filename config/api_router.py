from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from kkanbu.board.views import CategoryViewSet, CommentViewSet, PostViewSet
from kkanbu.notification.views import NotificationViewSet
from kkanbu.operation.views import CommentBlameViewSet, PostBlameViewSet
from kkanbu.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("category", CategoryViewSet)
router.register("post", PostViewSet)
router.register("comment", CommentViewSet)
router.register("postblame", PostBlameViewSet, basename="PostBlame")
router.register("commentblame", CommentBlameViewSet, basename="PostcommentBlame")
router.register("notification", NotificationViewSet, basename="Notification")

app_name = "api"

urlpatterns = [
    path("v1/", include(router.urls)),
]
