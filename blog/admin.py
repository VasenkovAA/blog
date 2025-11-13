from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from mdeditor.widgets import MDEditorWidget

from blog.models.post import Comment, Post
from blog.models.projects import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    formfield_overrides = {models.TextField: {"widget": MDEditorWidget}}
    autocomplete_fields = ["author"]

    def preview_tag(self, obj):
        if obj.preview:
            url = obj.preview.url
            return format_html('<a href="{}" target="_blank">Скачать</a>', url)
        return "Нет файла"

    preview_tag.short_description = "Предпросмотр"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
