from urllib.parse import urlencode

from rest_framework.exceptions import ValidationError

from kkanbu.board.models import Category


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def url_with_query(path, **kwargs):
    return path + "?" + urlencode(kwargs)


class TextLengthValidator:
    message = "제목과 내용은 4글자 이상 입력해 주세요."

    def __init__(self, min_length, message=None):
        self.min_length = min_length
        self.message = message or self.message

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(self.message)


class AppTypeValidator:
    message = "게시판에 알맞은 카테고리를 선택해주세요."

    def __init__(self, app_type, message=None):
        self.app_type = app_type
        self.message = message or self.message

    def __call__(self, value):
        # value = <class 'kkanbu.board.models.Category'> 카테고리 instance
        if not Category.objects.filter(app=self.app_type, slug=value.slug):
            raise ValidationError(self.message)
