import asyncio
import os
import subprocess
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. Настройка логирования
logging.basicConfig(level=logging.INFO)

# 2. Твой токен BIBABIT
TOKEN = "8275555421:AAHjuDjR2X5TWg6OU0rVM4E90kU1bBzk7A4"

# 3. Пути системы BIBABIT
# Определяем базу относительно файла бота (выходим из папки bot/ в корень)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRABBER_PATH = os.path.join(BASE_DIR, "grabber_v1.py")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

# Создаем папку music, если её нет
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

# Инициализируем бота
bot = Bot(token=TOKEN)

# Создаем роутер для команд
from aiogram import Router
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("비바비트 // BIBABIT SYSTEM ONLINE ♬\nПришли ссылку на Splice...")

@router.message()
async def handle_download(message: types.Message):
    if message.text and "splice.com" in message.text:
        await message.answer("📡 Сигнал принят. Запускаю перехват... (20 сек)")
        
        def run_grabber():
            try:
                subprocess.run(["python3", GRABBER_PATH, message.text], cwd=BASE_DIR, check=True)
            except Exception as e:
                print(f"Ошибка граббера: {e}")

        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, run_grabber)
            
            files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
            if files:
                last_file_path = max([os.path.join(MUSIC_DIR, f) for f in files], key=os.path.getmtime)
                audio_file = types.FSInputFile(last_file_path)
                await message.answer_audio(audio_file, caption=f"✅ BIBABIT // {os.path.basename(last_file_path)}")
            else:
                await message.answer("❌ Файл не найден. Проверь VPN.")
        except Exception as e:
            await message.answer(f"⚠️ Ошибка: {e}")

async def main():
    # Создаем Dispatcher строго ВНУТРИ асинхронного цикла
    dp = Dispatcher()
    dp.include_router(router)
    
    print("--- BIBABIT BOT STARTED ---")
    # Очищаем очередь обновлений и запускаем
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск асинхронного цикла
    asyncio.run(main())