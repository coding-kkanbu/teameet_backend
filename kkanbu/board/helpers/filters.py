from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework import filters
from rest_framework.compat import coreapi, coreschema


class TagFilter(filters.BaseFilterBackend):
    tag_param = "tags"
    tag_title = _("Tag")
    tag_description = _("The tags match.")

    def get_tag_terms(self, request):
        """
        Search terms are set by a ?tags=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.tag_param, "")
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        return params.split()

    def filter_queryset(self, request, queryset, view):
        tag_terms = self.get_tag_terms(request)

        if not tag_terms:
            return queryset

        queries = [Q(tags__name=tag_term) for tag_term in tag_terms]
        queryset_list = [queryset.filter(query) for query in queries]
        for q in queryset_list:
            queryset = queryset.intersection(q)
        return queryset

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=self.tag_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.tag_title),
                    description=force_str(self.tag_description),
                ),
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": self.tag_param,
                "required": False,
                "in": "query",
                "description": force_str(self.tag_description),
                "schema": {
                    "type": "string",
                },
            },
        ]


class PostOrderingFilter(filters.OrderingFilter):
    # The URL query parameter used for the ordering.
    ordering_param = "ordering"
    # TODO 두가지 필드 외에 FK로 연결된 postlike_n과 comment_n등도 필터링에 활용해보기
    ordering_fields = ["created", "hit"]
    # Default ordering attribute
    ordering = ["-created"]
