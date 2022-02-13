from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from kkanbu.board.views import CategoryViewSet, CommentViewSet, PostViewSet
from kkanbu.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("category", CategoryViewSet)
router.register("post", PostViewSet)
router.register("comment", CommentViewSet)


app_name = "api"

urlpatterns = [
    path("v1/", include(router.urls)),
]
