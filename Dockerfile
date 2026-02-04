FROM python:3.11-slim

# 1. Установка системных зависимостей для корректной работы Chromium
RUN apt-get update && apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Установка Python-библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Установка Playwright и Chromium (важно запускать через python -m)
RUN python -m playwright install chromium --with-deps

COPY . .

# 4. Открываем порт для Render
EXPOSE 8080

# 5. ГЛАВНОЕ: Запуск сервера и бота ОДНОВРЕМЕННО
# Мы используем '&', чтобы запустить app.py в фоне и сразу запустить бота
CMD python3 server/app.py & python3 bot/main_bot.py