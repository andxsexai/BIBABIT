import asyncio
import os
import sys
import logging
from playwright.async_api import async_playwright

async def intercept():
    if len(sys.argv) < 2:
        print("--- [ERROR] Нет ссылки для захвата ---")
        return
    url = sys.argv[1]
    
    # Путь к папке music в корне GANGPYTHON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(current_dir, "music")
    
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)

    captured = False

    async with async_playwright() as p:
        # Добавляем КРИТИЧЕСКИЕ флаги для работы в Docker/Render
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--no-zygote'
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        async def on_response(response):
            nonlocal captured
            # Перехват аудио-потоков
            content_type = response.headers.get("content-type", "")
            if "audio" in content_type or ".mp3" in response.url or "cdn-media" in response.url:
                try:
                    data = await response.body()
                    if len(data) < 30000: return 
                    
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
            print(f"[*] BIBABIT CLOUD: Загрузка {url}")
            # Увеличиваем таймаут для медленных серверов облака
            await page.goto(url, wait_until="networkidle", timeout=90000)
            
            # Попытка найти и нажать кнопку Play
            play_selectors = [
                "button[aria-label*='Play']",
                ".sp-player-button",
                "button:has-text('Play')",
                "[data-testid='play-button']"
            ]
            
            for selector in play_selectors:
                try:
                    btn = page.locator(selector).first
                    if await btn.is_visible():
                        await btn.click()
                        print(f"[*] BIBABIT: Кнопка {selector} нажата")
                        break
                except:
                    continue

            # Ожидание захвата (до 30 сек)
            for _ in range(60): 
                if captured:
                    break
                await asyncio.sleep(0.5)
                
        except Exception as e:
            print(f"--- [ERROR] Ошибка захвата: {e} ---")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(intercept())