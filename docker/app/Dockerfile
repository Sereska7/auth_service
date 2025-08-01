FROM python:3.12-slim-bookworm AS base

ENV TZ=UTC \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry=='2.0.0'

# Copy dependency files first to leverage caching
COPY poetry.lock pyproject.toml README.md ./

# **Скопировать папку app, чтобы poetry видел проект**
COPY app ./app

# Install dependencies and the project
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Скопировать остальные файлы, если есть (например, миграции, конфиги)
COPY . .
