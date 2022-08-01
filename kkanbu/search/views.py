from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet

from kkanbu.board.models import Post
from kkanbu.board.serializers import PostListSerializer


class TagFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get("tags")
        if tags is not None:
            queryset = queryset.filter(Q(tags__name__in=[tags])).distinct()
        return queryset


@extend_schema(tags=["search"])
class SearchViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Post.objects.filter(is_show=True)
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter, TagFilter]
    search_fields = ["title", "content"]
