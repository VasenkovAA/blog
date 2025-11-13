from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager

from blog.storages import get_private_storage


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    def validate_slug(value):
        if " " in value:
            raise ValidationError("Slug не может содержать пробелы")

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date="publish", validators=[validate_slug]
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blog_posts"
    )

    content = MDTextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    tags = TaggableManager(blank=True)

    preview = models.FileField(storage=get_private_storage, blank=True)

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish", "status"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "post": self.slug,
            },
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

    @classmethod
    def get_active_comments(cls):
        return cls.objects.select_related("post").filter(active=True)
