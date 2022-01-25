from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, MainListView  # PostViewSet,

router = DefaultRouter()
# router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)

app_name = "post"
urlpatterns = [
    url(r"^$", MainListView.as_view(), name="main"),
]

urlpatterns += router.urls
