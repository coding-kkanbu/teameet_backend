from django.contrib import admin

from .models import CommentBlame, PostBlame

admin.site.register(PostBlame)
admin.site.register(CommentBlame)
