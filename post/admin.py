from django.contrib import admin
from django.contrib import admin
from .models import Post,Like


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)


admin.site.register(Post, PostAdmin)
admin.site.register(Like)