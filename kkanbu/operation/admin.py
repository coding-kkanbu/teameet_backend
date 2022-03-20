from django.contrib import admin

from .models import CommentBlame, CommentLike, PostBlame, PostLike

admin.site.register([CommentLike, PostLike, CommentBlame, PostBlame])
