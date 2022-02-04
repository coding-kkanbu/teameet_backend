from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import BoardView, CommentViewSet  # PostViewSet

router = DefaultRouter()
# router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)

app_name = "board"
urlpatterns = [
    url(r"^$", BoardView.as_view(), name="board"),
]

urlpatterns += router.urls
