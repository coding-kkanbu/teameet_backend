from django.contrib import admin

from .models import Category, Comment, CommentLike, Post, PostLike, SogaetingOption, Tag

admin.register(Category)
admin.register(Post)
admin.register(PostLike)
admin.register(SogaetingOption)
admin.register(Comment)
admin.register(CommentLike)
admin.register(Tag)
