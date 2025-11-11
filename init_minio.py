import os

import django
from django_minio_backend import MinioBackend

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

try:
    minio_static = MinioBackend("staticfiles")
    minio_media = MinioBackend("default")
    print("MinIO buckets initialized successfully")
except Exception as e:
    print(f"MinIO initialization error: {e}")
