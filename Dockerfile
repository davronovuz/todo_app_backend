# Dockerfile

# Python rasmiy image
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# Atrof-muhit o'zgaruvchilari (Python tezroq ishlashi uchun)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Kerakli tizim kutubxonalarini o'rnatish (Postgres va boshqalar uchun)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Talablarni o'rnatish
COPY requirements/base.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Loyiha fayllarini ko'chirish
COPY . /app/

# Entrypoint skriptini ishga tushirish uchun ruxsat berish
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Entrypointni ishga tushirish
ENTRYPOINT ["/app/entrypoint.sh"]