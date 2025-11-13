import os

from django_minio_backend.models import MinioBackend
from dotenv import load_dotenv

load_dotenv(".env")
MINIO_MEDIA_BUCKET = os.getenv("MINIO_MEDIA_BUCKET", "django-media")
MINIO_STATIC_BUCKET = os.getenv("MINIO_STATIC_BUCKET", "django-static")


def get_public_storage():
    return MinioBackend(
        bucket_name=MINIO_MEDIA_BUCKET,
        storage_name="default",
    )


def get_private_storage():
    return MinioBackend(
        bucket_name=MINIO_STATIC_BUCKET,
        storage_name="default",
    )
