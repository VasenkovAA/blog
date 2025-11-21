from django.conf import settings
from django_minio_backend import MinioBackend, MinioBackendStatic


class CustomMinioBackendStatic(MinioBackendStatic):
    def url(self, name):
        if hasattr(settings, "STATIC_URL") and settings.STATIC_URL:
            return f"{settings.STATIC_URL}{name}"
        return super().url(name)


class CustomMinioBackend(MinioBackend):
    def url(self, name):
        if hasattr(settings, "MEDIA_URL") and settings.MEDIA_URL:
            return f"{settings.MEDIA_URL}{name}"
        return super().url(name)
