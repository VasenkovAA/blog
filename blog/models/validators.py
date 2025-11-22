from django.core.exceptions import ValidationError


def validate_slug_no_spaces(value: str) -> None:
    if ' ' in value:
        raise ValidationError('Slug не может содержать пробелы')
