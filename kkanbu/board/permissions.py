from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsOwnerOrReadOnly(IsAuthenticated):
    message = "글쓴이만 수정할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.writer == request.user or request.user.is_staff:
            return True
