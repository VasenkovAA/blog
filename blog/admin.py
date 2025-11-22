import io
import os
import shutil
import traceback

from django.contrib import admin, messages
from django.core.management import call_command
from django.db import models
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mdeditor.widgets import MDEditorWidget

from blog.models.backup import BackupLog
from blog.models.post import Comment, Post
from blog.models.projects import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "success", "message")
    readonly_fields = ("created_at", "success", "message")
    actions = ["create_backup_action"]

    @admin.action(description="Создать новый бэкап базы данных сейчас")
    def create_backup_action(self, request, queryset):
        pg_dump_path = shutil.which("pg_dump")
        env_path = os.environ.get("PATH", "PATH not set")

        print("--- DEBUG START ---")
        print(f"PG_DUMP PATH: {pg_dump_path}")
        print(f"SYSTEM PATH: {env_path}")

        log_buffer = io.StringIO()
        success = False

        try:
            if not pg_dump_path:
                raise Exception(f"CRITICAL: pg_dump не найден! PATH: {env_path}")

            print("Запуск dbbackup...")
            call_command("dbbackup", "--noinput", stdout=log_buffer, stderr=log_buffer)

            print("Команда выполнена.")
            success = True
            result_msg = f"SUCCESS LOG:\n{log_buffer.getvalue()}"

        except BaseException as e:
            success = False
            tb = traceback.format_exc()
            captured_log = log_buffer.getvalue()

            result_msg = (
                f"ERROR: {str(e)}\n"
                f"TYPE: {type(e)}\n"
                f"PG_DUMP LOCATION: {pg_dump_path}\n"
                f"CAPTURED LOGS:\n{captured_log}\n"
                f"TRACEBACK:\n{tb}"
            )
            print(f"--- CAUGHT EXCEPTION ---\n{result_msg}")

        try:
            BackupLog.objects.create(success=success, message=result_msg)
            if success:
                self.message_user(request, "Бэкап создан!", messages.SUCCESS)
            else:
                self.message_user(request, "Ошибка! См. лог в таблице.", messages.ERROR)
        except Exception as db_err:
            print(f"Ошибка при сохранении лога в БД: {db_err}")
            self.message_user(
                request,
                "Бэкап упал, и лог не сохранился. Смотри консоль Docker.",
                messages.ERROR,
            )

        print("--- DEBUG END ---")


class PostResource(resources.ModelResource):
    class Meta:
        model = Post


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource
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
