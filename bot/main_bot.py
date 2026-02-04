import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ (от @BotFather)
TOKEN = "ВАШ_ТОКЕН_ТУТ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🦾 GANGPYTHON SERVER ONLINE\nПришли ссылку на Splice, и я скачаю её в папку music.")

@dp.message()
async def download(message: types.Message):
    if "splice.com" in message.text:
        await message.answer("⏳ Запускаю граббер...")
        # Указываем полный путь к папке с музыкой
        output_dir = os.path.expanduser("~/Desktop/GANGPYTHON/music")
        # Запуск твоего граббера
        cmd = f"python3 ~/Desktop/GANGPYTHON/grabber_v1.py {message.text}"
        os.system(cmd)
        await message.answer(f"✅_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
