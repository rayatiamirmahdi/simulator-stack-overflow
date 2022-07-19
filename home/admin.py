from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'update')
    search_fields = ('slug', 'body')
    list_filter = ('update',)
    prepopulated_fields = {'slug': ('body',)}

admin.site.register(Post)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body[:20]', 'is_reply')
    list_filter = ('create', )


admin.site.register(Comment)
