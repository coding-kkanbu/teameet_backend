from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from kkanbu.operation.views import CommentBlameViewSet, PostBlameViewSet
from kkanbu.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("postblame", PostBlameViewSet, basename="PostBlame")
router.register("commentblame", CommentBlameViewSet, basename="PostcommentBlame")


app_name = "api"

urlpatterns = [
    path("board/", include("kkanbu.board.urls")),
    path("v1/", include(router.urls)),
]
