# Python 3.11 slim image'dan foydalanamiz
FROM python:3.11-slim

# Working directory o'rnatamiz
WORKDIR /app

# System dependencies o'rnatamiz
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Requirements faylini nusxalaymiz
COPY requirements.txt .

# Python kutubxonalarini o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalaymiz
COPY . .

# Static fayllarni yig'amiz
RUN python manage.py collectstatic --noinput

# Migratsiyalarni bajaramiz
RUN python manage.py migrate --noinput

# 8000 portni ochamiz
EXPOSE 8000

# Gunicorn bilan ishga tushiramiz
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]