from django.db import models


class BackupLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    class Meta:
        verbose_name = "Резервная копия"
        verbose_name_plural = "Резервные копии БД"

    def __str__(self):
        return f"Backup {self.created_at}"
