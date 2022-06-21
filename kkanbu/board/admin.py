from django.contrib import admin

from .models import Category, Comment, Post, SogaetingOption

admin.site.register([Category, Comment, Post, SogaetingOption])
