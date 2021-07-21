
from django.contrib import admin
from .models import Article, Comment, Profile

from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'status', 'pub_date')
    list_filter = ('status', 'pub_date')
    search_fields = ['title', 'content']

    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Article, PostAdmin)
admin.site.register(Profile)