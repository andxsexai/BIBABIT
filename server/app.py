from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import threading

app = Flask(__name__)

# --- ГЛОБАЛЬНАЯ КОРРЕКЦИЯ ПУТЕЙ ---
# Указываем на папку 'server'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Выходим на уровень выше в корень 'GANGPYTHON'
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# Папка с музыкой теперь всегда в корне проекта
MUSIC_DIR = os.path.join(PROJECT_ROOT, 'music')

if not os.path.exists(MUSIC_DIR): 
    os.makedirs(MUSIC_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")
    if not url: 
        return jsonify({"status": "error", "message": "URL не указан"}), 400
    
    def run_grabber():
        try:
            # Находим grabber_v1.py строго в корне проекта
            grabber_path = os.path.join(PROJECT_ROOT, "grabber_v1.py")
            
            # Запускаем, принудительно устанавливая рабочую директорию в корень
            # Это гарантирует, что граббер сохранит файл в PROJECT_ROOT/music
            subprocess.run(
                ["python3", grabber_path, url], 
                check=True, 
                cwd=PROJECT_ROOT
            )
            print(f"--- [OK] ЗАХВАТ ЗАВЕРШЕН ДЛЯ: {url}")
        except Exception as e:
            print(f"--- [ERROR] ОШИБКА ПУТИ ИЛИ ГРАББЕРА: {e}")

    # Запускаем в фоновом потоке, чтобы не вешать сайт
    threading.Thread(target=run_grabber, daemon=True).start()
    return jsonify({"status": "success", "message": "Процесс запущен"})

@app.route("/files")
def list_files():
    if not os.path.exists(MUSIC_DIR): return jsonify([])
    # Сортировка: самые новые файлы в топе
    files = sorted(
        [f for f in os.listdir(MUSIC_DIR) if f.endswith((".mp3", ".wav"))], 
        key=lambda x: os.path.getmtime(os.path.join(MUSIC_DIR, x)), 
        reverse=True
    )
    return jsonify(files)

@app.route("/listen/<path:filename>")
def listen(filename):
    return send_from_directory(MUSIC_DIR, filename)

if __name__ == "__main__":
    print(f"--- GANGPYTHON HOST АКТИВИРОВАН ---")
    print(f"--- КОРЕНЬ ПРОЕКТА: {PROJECT_ROOT}")
    app.run(host="0.0.0.0", port=8080)