import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def intercept():
    if len(sys.argv) < 2:
        print("--- [ERROR] Нет ссылки для захвата ---")
        return
    url = sys.argv[1]
    
    # Определяем путь к папке music в корне проекта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(current_dir, "music")
    
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)

    captured = False

    async with async_playwright() as p:
        # headless=True КРИТИЧНО для Render (облака без монитора)
        browser = await p.chromium.launch(headless=True) 
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        async def on_response(response):
            nonlocal captured
            # Фильтр для аудио-потоков Splice
            content_type = response.headers.get("content-type", "")
            if "audio" in content_type or ".mp3" in response.url or "cdn-media" in response.url:
                try:
                    data = await response.body()
                    if len(data) < 30000: return # Игнорируем мелкие системные звуки
                    
                    filename = f"GANG_SAMPLE_{os.urandom(2).hex()}.mp3"
                    filepath = os.path.join(music_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(data)
                    
                    print(f"--- [OK] ПЕРЕХВАЧЕНО: {filename} ---")
                    captured = True 
                except:
                    pass

        page.on("response", on_response)
        
        try:
            print(f"[*] BIBABIT CLOUD: Открываю {url}")
            # Переходим на страницу
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Пытаемся нажать кнопку Play автоматически
            # Splice часто использует aria-label="Play" или иконки
            play_buttons = [
                page.get_by_label("Play", exact=False),
                page.locator("button:has-text('Play')"),
                page.locator(".sp-player-button") # Распространенный класс
            ]
            
            for btn in play_buttons:
                try:
                    if await btn.is_visible():
                        await btn.click()
                        print("[*] Авто-воспроизведение активировано")
                        break
                except:
                    continue

            # Ждем перехвата до 20 секунд
            for _ in range(40): 
                if captured:
                    break
                await asyncio.sleep(0.5)
                
        except Exception as e:
            print(f"--- [ERROR] Ошибка захвата: {e} ---")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(intercept())