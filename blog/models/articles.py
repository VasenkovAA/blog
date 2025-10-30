from django.db import models


class ArticleGroup(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название группы",
    )

    class Meta:
        verbose_name = "Группа статей"
        verbose_name_plural = "Группы статей"

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название статьи",
    )
    description = models.TextField(
        verbose_name="Описание статьи",
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        ArticleGroup,
        on_delete=models.PROTECT,
        verbose_name="Группа",
        related_name="articles",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
