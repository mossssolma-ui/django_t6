from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_published", "count_views", "created_at", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
