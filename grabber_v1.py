import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def intercept():
    if len(sys.argv) < 2:
        return
    url = sys.argv[1]
    
    # Определяем путь к папке music в корне GANGPYTHON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(current_dir, "music")
    
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)

    # Флаг для ускоренного выхода
    captured = False

    async with async_playwright() as p:
        # headless=False важен для ручного нажатия Play
        browser = await p.chromium.launch(headless=False) 
        context = await browser.new_context()
        page = await context.new_page()

        async def on_response(response):
            nonlocal captured
            # Расширенный фильтр для Splice CDN и аудио-типов
            content_type = response.headers.get("content-type", "")
            if "audio" in content_type or ".mp3" in response.url or "cdn-media" in response.url or "wav" in response.url:
                try:
                    data = await response.body()
                    if len(data) < 20000: return # Пропускаем системные звуки
                    
                    filename = f"GANG_SAMPLE_{os.urandom(2).hex()}.mp3"
                    filepath = os.path.join(music_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(data)
                    
                    print(f"--- [OK] ПЕРЕХВАЧЕНО: {filename} ---")
                    captured = True # Даем сигнал на выход
                except:
                    pass

        page.on("response", on_response)
        
        try:
            print(f"[*] Открываю: {url}")
            # Ожидаем загрузки структуры страницы
            await page.goto(url, wait_until="domcontentloaded")
            
            print("[*] Жду нажатия PLAY. У тебя есть 20 секунд.")
            
            # Ускоренный цикл: проверяем наличие файла каждые 0.5 сек
            for _ in range(40): 
                if captured:
                    print("[*] Файл пойман! Закрываю браузер...")
                    break
                await asyncio.sleep(0.5)
                
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(intercept())