from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BoardView, CommentViewSet, PostView, TopicView  # PostViewSet

router = DefaultRouter()
# router.register(r"post", PostViewSet)
router.register(r"comment", CommentViewSet)

app_name = "board"
urlpatterns = [
    path("", BoardView.as_view(), name="board"),
    path("topic/<str:slug>/", TopicView.as_view(), name="topic"),
    path("post/<int:pk>/", PostView.as_view(), name="post"),
]

urlpatterns += router.urls
