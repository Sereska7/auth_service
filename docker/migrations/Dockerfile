FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry=='2.0.0'

WORKDIR /migrations

# Копируем файлы зависимостей
COPY poetry.lock pyproject.toml README.md ./

# Копируем код приложения, который лежит в корне, папку app
COPY app ./app

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные миграционные скрипты
COPY . .
