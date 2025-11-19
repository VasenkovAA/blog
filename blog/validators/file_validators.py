import os

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class FileSizeValidator(BaseValidator):
    """
    Сериализуемый валидатор размера файла
    """

    message = _("Файл слишком большой. Максимальный размер: %(max_size)s MB")
    code = "file_size"

    def __init__(self, max_size=5 * 1024 * 1024):
        self.max_size = max_size
        super().__init__(max_size)

    def __call__(self, value):
        if value.size > self.max_size:
            params = {"max_size": self.max_size // (1024 * 1024)}
            raise ValidationError(self.message, code=self.code, params=params)

    def clean(self, value):
        return value.size

    def compare(self, a, b):
        return a > b


def validate_image_extension(value):
    """
    Функция-валидатор для расширений файлов (сериализуема)
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

    if ext not in valid_extensions:
        raise ValidationError(
            _("Неподдерживаемое расширение файла. Разрешены: %(extensions)s"),
            params={"extensions": ", ".join(valid_extensions)},
        )
