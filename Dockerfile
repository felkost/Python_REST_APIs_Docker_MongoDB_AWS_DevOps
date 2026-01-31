# 1) Базовий образ з Python (легкий)
FROM python:3.12-slim

# 2) Базові налаштування Python (зручно для контейнера)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3) Робоча директорія всередині контейнера
WORKDIR /app

# 4) Встановлюємо uv (можна й multi-stage, але для простоти так)
RUN pip install --no-cache-dir uv

# 5) Копіюємо лише файли залежностей (для кешування шарів)
COPY pyproject.toml uv.lock ./

# 6) Ставимо залежності З LOCK-файлу, але НЕ встановлюємо сам проєкт
#    --frozen: не дозволяє змінювати uv.lock під час білду
#    --no-dev: не ставити dev-залежності (якщо з’являться)
#    --no-install-project: НЕ збирати/ставити ваш пакет (бо src ще не скопійовано)
RUN uv sync --frozen --no-dev --no-install-project

# 7) Тепер копіюємо все
COPY . .

# 8) Щоб Python бачив модулі з /app/src
ENV PYTHONPATH=/app/src

# 9) Відкриваємо порт (документація, не “мапінг”)
EXPOSE 5000

# 10) Продакшн-сервер (gunicorn) запускає WSGI app об'єкт "app"
#     Важливо: 0.0.0.0, щоб контейнер слухав зовнішні підключення
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0:5000", "python_rest_apis_docker_mongodb_aws_devops.app:app"]
