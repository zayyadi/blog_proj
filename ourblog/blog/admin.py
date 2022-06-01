from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Article, Category, Comment


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'status', 'publish')
    list_filter = ('status', 'publish')
    search_fields = ['title', 'content']

    summernote_fields = ('content',)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('author', 'body', 'post', 'created_on', 'active')
#     list_filter = ('active', 'created_on')
#     search_fields = ('author', 'email', 'body')
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)


admin.site.register(Article, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, MPTTModelAdmin)
