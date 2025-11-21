FROM python:3.11-slim as builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    locales \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen ru_RU.UTF-8

ENV LC_ALL=ru_RU.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY --from=builder /install /usr/local

COPY --chown=app:app . .

USER app

RUN python -c "import django; print(f'✅ Django {django.__version__}')" && \
    python -c "import requests; print('✅ Requests installed')" && \
    python -c "import minio; print('✅ MinIO client installed')"

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-"]
