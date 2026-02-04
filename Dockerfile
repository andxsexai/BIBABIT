FROM python:3.11-slim

# Установка системных библиотек
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Устанавливаем gunicorn для стабильности веб-сервера
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Установка Playwright
RUN python -m playwright install chromium --with-deps

COPY . .

# Создаем папку music заранее, чтобы не было ошибок доступа
RUN mkdir -p music

EXPOSE 8080

# Запуск: Сначала бот в фоне, затем веб-сервер gunicorn
CMD python3 bot/main_bot.py & gunicorn --bind 0.0.0.0:8080 server.app:app