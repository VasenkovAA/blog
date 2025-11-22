from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Название проекта',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание проекта',
    )
    link = models.URLField(
        blank=True,
        verbose_name='Ссылка на проект',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='blog_projects'
    )
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'author']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f'{self.name} (by {self.author.username})'
