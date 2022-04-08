from rest_framework.pagination import PageNumberPagination


class NotiPageNumberPagination(PageNumberPagination):
    page_size = 20
