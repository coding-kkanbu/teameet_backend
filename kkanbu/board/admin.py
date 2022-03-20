from django.contrib import admin

from .models import Category, Comment, Post, SogaetingOption, Tag

admin.site.register([Category, Comment, Post, SogaetingOption, Tag])
