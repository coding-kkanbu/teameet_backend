from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from kkanbu.board.models import Category, Post


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    introduce = "좋은 만남을 기대하고있습니다"

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("name")
    slug = Faker("slug")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    category = factory.SubFactory(CategoryFactory)
    writer = factory.SubFactory(UserFactory)
