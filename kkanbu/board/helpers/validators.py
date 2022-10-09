from rest_framework.exceptions import ValidationError

from kkanbu.board.models import Category


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
        if not Category.objects.filter(app=self.app_type, name=value.name):
            raise ValidationError(self.message)
