import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["POST"],
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
