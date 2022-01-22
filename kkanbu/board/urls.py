from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostCreateView, PostListView  # PostViewSet,

router = DefaultRouter()
# router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)


urlpatterns = [
    re_path(r"^$", PostListView.as_view(), name="list"),
    re_path(r"^create/$", PostCreateView.as_view(), name="create"),
]

urlpatterns += router.urls
