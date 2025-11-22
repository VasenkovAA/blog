from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from blog.models.validators import validate_slug_no_spaces


class ArticleGroup(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название группы',
    )

    class Meta:
        verbose_name = 'Группа статей'
        verbose_name_plural = 'Группы статей'

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date='publish', validators=[validate_slug_no_spaces]
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='blog_article'
    )

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    group = models.ForeignKey(
        ArticleGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='Группа статей',
    )
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created']

    def __str__(self):
        return self.title
