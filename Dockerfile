# Многостадийная сборка для оптимизации
FROM python:3.11-slim as builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Установка только системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости в отдельную директорию
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Финальный образ
FROM python:3.11-slim

# Устанавливаем локаль
RUN apt-get update && apt-get install -y \
    locales \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen ru_RU.UTF-8

ENV LC_ALL=ru_RU.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Создаем не-root пользователя
RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

# Копируем установленные пакеты из builder в системные пути
COPY --from=builder /install /usr/local

# Копируем код приложения
COPY --chown=app:app . .

# Меняем владельца и переключаемся на не-root пользователя
USER app

# Проверяем что зависимости установлены
RUN python -c "import django; print(f'✅ Django {django.__version__}')" && \
    python -c "import requests; print('✅ Requests installed')" && \
    python -c "import minio; print('✅ MinIO client installed')"

# Проверяем здоровье
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000

# Запускаем через gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-"]
