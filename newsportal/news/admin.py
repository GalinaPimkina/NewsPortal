from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'time_create']
    list_filter = ['author', 'time_create']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
