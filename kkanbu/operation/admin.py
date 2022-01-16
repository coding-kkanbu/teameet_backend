from django.contrib import admin

from .models import CommentBlame, PostBlame

admin.register(PostBlame)
admin.register(CommentBlame)
