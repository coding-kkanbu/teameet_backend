from django.contrib import admin

from .models import Category, Comment, CommentLike, Post, PostLike, SogaetingOption, Tag

admin.site.register(
    [Category, Comment, CommentLike, Post, PostLike, SogaetingOption, Tag]
)
