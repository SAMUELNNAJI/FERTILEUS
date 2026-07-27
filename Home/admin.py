from django.contrib import admin
from .models import Blog, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display  = ('blog_title', 'blog_category', 'blog_author', 'blog_date', 'published')
    list_filter   = ('blog_category', 'published', 'blog_date')
    search_fields = ('blog_title', 'blog_author', 'blog_content')
    prepopulated_fields = {'blog_slug': ('blog_title',)}
    list_editable = ('published',)
    date_hierarchy = 'blog_date'
    ordering = ('-blog_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'blog', 'created', 'approved', 'likes')
    list_filter   = ('approved', 'created')
    search_fields = ('name', 'body')
    list_editable = ('approved',)
    ordering = ('-created',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'
