from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import BoardListView, CommentViewSet  # PostViewSet,

router = DefaultRouter()
# router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)

app_name = "post"
urlpatterns = [
    url(r"^$", BoardListView.as_view(), name="main_board"),
]

urlpatterns += router.urls
